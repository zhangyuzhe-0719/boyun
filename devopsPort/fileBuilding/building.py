import os

def get_fileSize(size):
    '''
    根据传入参数,生成指定大小的文件
    :param size: 默认单位为mb
    :return:
    '''
    excepSize = size * 1024 * 1024 - 1
    path = os.path.join(os.path.dirname(__file__),'ceshi.txt')
    filesize = 0
    while filesize <= excepSize:
        with open(file=path,mode='a+',encoding='utf-8') as fw:
            filesize = os.path.getsize(path)
            file = excepSize - filesize
            if file > 100:
                fw.write('s'*100)
            else:
                fw.write('s')
    print('生成完毕 期望大小{} 实际大小{}'.format(excepSize,filesize))

if __name__ == '__main__':
    get_fileSize(50)