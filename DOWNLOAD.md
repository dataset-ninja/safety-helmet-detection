Dataset **Safety Helmet Detection** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/Y/R/6q/Z7pqUp9Cafh2oii50bADaauH2hGdjrdkMMzc49fGhx7ziTPY5tnHXfjcQRjFBBLnteN7cZEHPdZ4xWL7raIH3ub0iXIPUI88hYTj13Sv4uy7clA9DZpZK1XGjUg3.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Safety Helmet Detection', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection/download?datasetVersionNumber=1).