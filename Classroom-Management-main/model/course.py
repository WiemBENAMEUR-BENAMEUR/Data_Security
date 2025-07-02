import re
import os
import json
from lib.helper import course_data_path
from lib.helper import user_data_path
from lib.helper import course_json_files_path


class Course:

    def __init__(self, catitle="",idcat=-1,subtitle="",course_id=-1, course_title="",url="",course_num_subscribers=-1,course_avg_rating=-1, number_reviews=-1):

        self.catitle=catitle
        self.idcat=idcat
        self.subtitle=subtitle
        self.url=url
        self.number_reviews=number_reviews

        self.course_id = course_id
        self.course_title = course_title

        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating


    def __str__(self):
        pass

    def get_courses(self):
        t = []
        a = set([])
        for dirs in os.listdir(course_json_files_path):
            # print(dirs)
            for dirssub in os.listdir(course_json_files_path +"/"+ dirs):
                # print(dirssub)
                for file in os.listdir(course_json_files_path +"/" +dirs + "/" + dirssub):
                    with open(course_json_files_path +"/"+ dirs + "/" + dirssub + "/" + file,
                              encoding="ISO-8859-1") as f:
                        fin = f.read()
                        # print(len(fin))

                        lst = []

                        idsubcat = re.findall('{"category":.*?"id": ([0-9]+)', fin)
                        # print(idsubcat)
                        a = re.findall('"items(.*)remaining_item_count"', fin)
                        b = a[0].replace(":[", "").replace("],", "")
                        # print(b)
                        t.append(b.replace("{", "").replace("}", "").replace("\"", ""))

                        for i in t:
                            # print(i)
                            courseid = re.findall('_class: course, id: ([0-9]+),', i)
                            # for i in courseid:
                            # a.append(i)
                            coursetitle = re.findall('_class: course, id: [0-9]+, title: (.*?), url: /course/', i)
                            # print(len(coursetitle))
                            avg_rating = re.findall('avg_rating: (.*?), avg_rating_recent:', i)
                            # print(len(avg_rating))
                            url = re.findall('url: (.*?),', i)
                            # print(len(url))
                            num_subs = re.findall('headline:.*?, num_subscribers: (.*?), caption_locales', i)
                            # print(len(num_subs))
                            num_reviews = re.findall('num_reviews: (.*?),', i)
                            # print(len(num_reviews))


                        with open(course_data_path, 'a+', encoding="utf8") as coursefile:
                            for j in range(16):
                                if (len(courseid) == 16 & len(coursetitle) == 16 & len(url) == 16 & len(
                                        num_subs) == 16 & len(avg_rating) == 16 & len(num_reviews) == 16):
                                    coursefile.writelines(dirs + ";;;" + idsubcat[0] + ";;;" + dirssub + ";;;" +
                                                          courseid[j] + ";;;" + coursetitle[j] + ";;;"  + url[
                                                              j] + ";;;" +
                                                          num_subs[j] + ";;;" + avg_rating[j] + ";;;" + num_reviews[
                                                              j] + '\n')
        pass

    def getlistcourse(self):
        List = []

        with open(course_data_path, "r", encoding="utf8") as fi:
            filelinesins = fi.readlines()
            for obj in filelinesins:
                inst = obj.strip().split(";;;")

                a = Course(inst[0], inst[1], inst[2],inst[3],inst[4],inst[5],inst[6],inst[7],inst[8])
                List.append(a.toJSON())
        return List


    def generate_page_num_list(self, page, total_pages):
        pass

    def get_courses_by_page(self, page):
        pass

    def delete_course_by_id(self, temp_course_id):
        with open(course_data_path, "r") as infile:
            lines = infile.readlines()

        with open(course_data_path, "w") as outfile:
            for line in lines:
                inst = line.strip().split(";;;")
                if (inst[3] != temp_course_id):
                    outfile.write(line)


        pass

    def get_course_by_course_id(self, temp_course_id):
        with open(course_data_path, "r", encoding="utf8") as fi:
            f=fi.readlines()
            for h in f:
                inst=h.strip().split(";;;")

                if(inst[3]==temp_course_id):
                    a=Course(inst[0], int(inst[1]), inst[2],int(inst[3]),inst[4],inst[5],inst[6],inst[7],inst[8])
                    return a.toJSON()


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
