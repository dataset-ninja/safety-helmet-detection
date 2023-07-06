Dataset **Safety Helmet Detection** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/4/C/o2/UUUqfWeuVUhMJwRhHAOm8Hg1vuNemHW18jK9qaRZJL5vmQDuRYJIOkYlRGwD8FzY2V6HP2eobwwW80NCDFcO5lIL7X2NJMicvMA15UvEkypFGdFFMmb0zkU9lIQQ.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Safety Helmet Detection', dst_path='~/dtools/datasets/Safety Helmet Detection.tar')
```
The data in original format can be 🔗[downloaded here](https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection/download?datasetVersionNumber=1)