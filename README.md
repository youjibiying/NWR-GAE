# NWR-GAE

An implementation of ICLR 2022 Paper: [Graph Auto-Encoder via Neighborhood Wasserstein Reconstruction]
(https://openreview.net/forum?id=ATUh28lnSuW)

## Required Packages

Before to execute NWR-GAE, it is necessary to install the following packages using requirments.txt:

`pip install -r requirements.txt`

## Overall Structure

The repository is organised as follows:
- `data/` contains the necessary python files for generating synthetic data;
- `datasets/` contains the necessary dataset files for real-world datasets;
- `edgelists/` contains the necessary dataset files for real-world datasets in edgelist format;
- `src/` contains the implementation of the NW-GAE pipeline (`model.py`) and our training file (`train.py`);
- `src/layers` contains the network layers, such as MLP, PairNorm (`layers.py`).
- `src/utils` contains the necessary processing subroutines (`utils.py`).

## Basic Usage
### Support Datasets
**Proximity:** cora, citeseer, pubmed

**Structure:** cornell, texas, wisconsin

**Mixed:** chameleon, squirrel, film (actor)

**Synthetic:** generated from https://github.com/snap-stanford/graphwave

### Support Parameters
**--dataset**, supported datasets above, default: texas

**--lr**, learning rate for neighborhood reconstructor, default: 5e-5

**--epoch_num**, training epoch size, default: 100

**--lambda_loss1**, balance weights for degree and neighborhood information decoder, default: 1e-2

**--lambda_loss2**, balance weights for feature decoder, default: 1e-2

**--sample_size**, size of neighborhood down sampling, default: 5

**--dimension**, dimension of final output embeddings, default: 1500

### Example

```bash
cd src
python train.py --dataset texas # real-world datasets
python train.py --dataset_type synthetic # Synthetic datasets
```

, the default setting can run most of the state-of-art results (especially on structure-oriented/mixed datasets, i.e. cornell, texas, wisconsin). 
