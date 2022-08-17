import os
import re


def rename(file_name,path):
    result = re.match("^\d{1,}", file_name, re.I|re.M)
    if  result is not  None:
        new_file_name = re.sub("^\d{1,}", "", file_name, count=0, flags=0)
        new_file_name = new_file_name.replace(' ','')
        # print("new_file_name",new_file_name)
        old_full_path = os.path.join(path, file_name)
        new_full_path = os.path.join(path, new_file_name)
        os.rename(old_full_path,new_full_path)
        print("旧版本 %s,替换为：%s" % (file_name,new_file_name))
        
def main():
    # 遍历文件夹
    g = os.walk(os.getcwd())
    for path,dir_list,file_list in g:
        for file_name in file_list:
            if file_name.endswith(".md"):
                
                rename(file_name,path)
            


if __name__ == "__main__":
    main()
