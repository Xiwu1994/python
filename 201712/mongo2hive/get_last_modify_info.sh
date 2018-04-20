#!/bin/bash

FILE_PATH="/Users/liebaomac/PhpstormProjects/beeper_base_api/models"
cd ${FILE_PATH}

# 换git log 日期格式
# Date:   2017-12-16 16:27:14 +0800
git config log.date iso8601

for file in $(ls)
do
  modify_date=`git log -1 ${file} | grep Date | awk 'BEGIN{FS="   "}{print $2}' | awk '{print $1}'`
  modify_person=`git log -1 ${file} | grep Author | awk 'BEGIN{FS="Author: "}{print $2}' | awk 'BEGIN{FS=" <"}{print $1}'`
  echo -e ${file}"\t"${modify_date}"\t"${modify_person}
  break
done

