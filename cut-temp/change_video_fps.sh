IN_DATA_DIR="./video_crop_25"
OUT_DATA_DIR="./video_crop_30"

if [[ ! -d "${OUT_DATA_DIR}" ]]; then
  echo "${OUT_DATA_DIR} doesn't exist. Creating it.";
  mkdir -p ${OUT_DATA_DIR}
fi

for video in $(ls -A1 -U ${IN_DATA_DIR}/*)
do
  video_name=${video##*/}

  echo $video_name
  array=(${video_name//./ })
  video_name=${array[0]}
  echo $video_name
    

  out_video_dir=${OUT_DATA_DIR}/${video_name}.mp4


  ffmpeg -i "${video}" -r 30 -q:v 1 "${out_video_dir}"
done