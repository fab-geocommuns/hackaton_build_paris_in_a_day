# Projet de reconstitution de scene 3D en utilisant des photos Panoramax et Nerfstudio

## Installation

Installation de [nerfstudio](https://docs.nerf.studio/):

```bash
uv venv --python 3.11
uv pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
uv pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
uv pip install "numpy < 2"
uv pip install nerfstudio

sudo apt update
sudo apt install colmap
```

# récupération de données

Récupération de données sur strasbourg (bonne densité de couverture et qualité d'image).

récupération des images via le script duckdb

```duckdb
copy(
    SELECT
        id,
        geometry, -- position de l'image
        datetime, -- date de prise de vue
        assets[1].href as image_url -- url de l'image
    FROM
        'https://api.panoramax.xyz/data/geoparquet/panoramax.parquet'
    WHERE
        bbox.xmin > 7.742269
        and bbox.ymin > 48.581608
        and bbox.xmax < 7.743224
        and bbox.ymax < 48.582041
) to '~/dev/ign/hackaton_2026/strasbourg.csv';
```

puis téléchargement des images dans un repertoire `pics/strasbourg/`.

# Préparation des données

On crop 20% de l'image en bas, pour virer le logo de la ville

```
time uv run ns-process-data images \
--camera-type equirectangular \
--images-per-equirect 8 \
--data pics/strasbourg/ \
 --output-dir pics/processed \
 --crop-factor 0 0.2 0 0 
```

