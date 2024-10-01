---
id: 1535
title: 'Dynamic sparse build matrices in Github Actions'
date: '2024-04-29T00:42:25+10:00'
author: 'Olivier Mehani'
excerpt: 'GitHub Actions support matrix jobs, allowing to build codebase across multiple parameters. It is also possible to generate dynamic subsets of those parameters using a simple Python script based on intput to a user-dispatchable workflow.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1535'
permalink: '/?p=1535'
---

[GitHub Actions support matrix jobs](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs). Those are handy to build or test a codebase across a combination of multiple parameters. The mechanism is fairly extensible, and [additional parameters can be selectively added to the generated combinations](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#expanding-or-adding-matrix-configurations). The system, however is geared towards generating all the combinations on every run.

In some situations, one may want to only run a subset of the whole matrix, such as building all architectures for one operating system, or deploying all relevant components to a single specific region. Fortunately, GitHub Action jobs can also [obtain their configuration from an arbitrary JSON string](https://docs.github.com/en/actions/learn-github-actions/expressions#fromjson). It is therefore possible to [use a script to generate a dynamic matrix](https://stackoverflow.com/questions/59977364/github-actions-how-use-strategy-matrix-with-script) of job parameters based on user-selectable parameters to the workflow.

tl;dr:

- With the example of a multi-region, multi-component deployment (where the components to deploy vary per region),
- it is possible to create a user-dispatchable workflow which allows the user to deploy, everything, or select a single region or component to deploy
- with a simple Python script outputing the build matrix selectively.

The Python script is pretty straightforward to write. It needs to have a full list of the dimensions of the matrix, and their mapping, *i.e.*, component to region. A function can then take user-provided arguments for the components and regions, both of which can be `all`, and filter the full mapping accordingly, before returning it as a JSON object.

```
#!/usr/bin/env python3
#
# Utility to generate deployment matrices suitable for Github Actions Workflows.
#
# /!\ All error handling removed for brevity!
#

import json
import sys

ALL_REGIONS = [ 'ap-southeast-2', 'us-east-1', 'us-west-1' ]

COMPONENT_REGIONS = {
    'database': [ 'us-east-1' ],
    'maintenance': ['ap-southeast-2', 'us-west-1'],
    'web': ALL_REGIONS,
}

def filter_component_regions(component: str, region: str) -> dict:
    component_regions = COMPONENT_REGIONS.copy()

    if component != 'all':
        component_regions = { component: component_regions[component] }

    if region != 'all':
        component_regions = { c: [r
                                for r in component_regions[c]
                                if r == region]
                           for c in component_regions}

    return component_regions

if __name__ == '__main__':
    print(json.dumps(filter_component_regions(sys.argv[1], sys.argv[2])))
```

<div class="wp-block-image"><figure class="aligncenter size-full">![Screenshot of a terminal showing example outputs of the sparse matrix generation script](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/04/Screenshot-from-2024-04-29-00-16-31.png)</figure></div>The rest of the logic is in a dispatchable workflow. It offers two `choice` inputs with all the supported values, including `all` for the `component` and `region` parameters. It comprises two jobs: the first one passes the input to the matrix-generation script, and stores the JSON output into a variable. The second job is the release job itself, parametrised via two arguments. The arguments are populated with the `matrix` strategy, the data for which comes from an `include` using the `fromJSON` method on the previously generated variable.

```
name: deploy
on:
  workflow_dispatch:
    inputs:
      component:
        description: Component to deploy
        type: choice
        options:
          - all
          - database
          - maintenance
          - web
      region:
        description: Region to deploy
        type: choice
        options:
          - all
          - ap-southeast-2
          - us-east-1
          - us-west-1

jobs:
  release-matrix:
    name: Generate release matrix
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          echo "matrix=$( \
                python .github/workflows/release_matrix.py \
                  ${{ github.event.inputs.service}} \
                  ${{ github.event.inputs.region }} \
          )" >> "${GITHUB_OUTPUT}"

  regions-release:
    name: Release
    runs-on: ubuntu-latest
    needs: [release-matrix]
    strategy:
      matrix:
        include: ${{ fromJSON(needs.release-matrix.outputs.matrix) }}

    steps:
      - name: Release
        id: release
        uses: private/release
        with:
          component: ${{ matrix.component }}
          region: ${{ matrix.region }}
```

It should be reasonably easy to expand to more than 2 dimensions. The exercise is left to the reader (potentially future me, when it turns out I need this).