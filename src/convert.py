import os
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name, get_file_size
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)
        fsize = get_file_size(local_path)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer..", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = get_file_size(local_path)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer {local_path}...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    dataset_path = "/Users/iwatkot/Downloads/ninja/datasets/safety-helmet"
    images_folder = "images"
    bboxes_folder = "annotations"
    bboxes_ext = ".xml"
    ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        labels = []

        file_name = get_file_name(image_path)

        ann_path = os.path.join(bboxes_path, file_name + bboxes_ext)

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            img_height = int(root.find(".//height").text)
            img_wight = int(root.find(".//width").text)

            objects = root.findall(".//object")
            for curr_obj in objects:
                name = curr_obj.find(".//name").text
                obj_class = meta.get_obj_class(name)
                curr_coord = curr_obj.find(".//bndbox")
                left = int(curr_coord[0].text)
                top = int(curr_coord[1].text)
                right = int(curr_coord[2].text)
                bottom = int(curr_coord[3].text)

                rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                label = sly.Label(rect, obj_class)
                labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class_helmet = sly.ObjClass("helmet", sly.Rectangle)
    obj_class_person = sly.ObjClass("person", sly.Rectangle)
    obj_class_head = sly.ObjClass("head", sly.Rectangle)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(obj_classes=[obj_class_helmet, obj_class_person, obj_class_head])
    api.project.update_meta(project.id, meta.to_json())

    images_path = os.path.join(dataset_path, images_folder)
    bboxes_path = os.path.join(dataset_path, bboxes_folder)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_names = [im_name for im_name in os.listdir(images_path)]

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for images_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [os.path.join(images_path, im_name) for im_name in images_names_batch]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in images_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(images_names_batch))

    return project
