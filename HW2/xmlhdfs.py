import sys
from lxml import etree
import datetime

fsimage = r'C:\Ava\USC\DSCI551\HW_lab\homework2\fsimage564.xml'
dir = '/user/ec2-user/dsci551/input/core-site.xml'

fsimage = sys.argv[1]
dir = sys.argv[2]


def decode(elems):
    if (isinstance(elems, list)):
        res = []
        for elem in elems:
            if isinstance(elem, str):
                res.append(elem)
            else:
                res.append(elem.xpath('string(.)').strip())

    else:
        res = elems.xpath('string(.)').strip()
    return res[0] if len(res)==1 else res


def translate_mode(permission):
    res = ''
    for octal in permission[1:]:
        if octal == '7':
            res += 'rwx'
        elif octal == '6':
            res += 'rw-'
        elif octal == '5':
            res += 'r-x'
        elif octal == '4':
            res += 'r--'
        elif octal == '3':
            res += '-wx'
        elif octal == '2':
            res += '-w-'
        elif octal == '1':
            res += '--x'
        elif octal == '0':
            res += '---'
    return res



tree = etree.parse(open(fsimage))
split_dirs = dir.split('/')
if len(split_dirs) > 1 and split_dirs[-1] == '':
    split_dirs = split_dirs[:-1]
    dir = ('/').join(split_dirs)
steps = len(split_dirs)
step = 0
split_dir_id = decode(tree.xpath('//INodeSection/inode[name="{}"]/id'.format(split_dirs[step])))
while step < steps - 1:
    child_nodes_id = decode(tree.xpath('//INodeDirectorySection/directory[parent="{}"]/child'.format(split_dir_id)))
    tmp_dir_id = split_dir_id
    child_nodes_id = [child_nodes_id] if isinstance(child_nodes_id, str) else child_nodes_id
    step += 1
    for node in child_nodes_id:
        file_name = decode(tree.xpath('//INodeSection/inode[id="{}"]/name'.format(node)))
        if file_name == split_dirs[step]:
            split_dir_id = node
            break
    if tmp_dir_id == split_dir_id:
        step = steps

if step == steps:
    print('ls: {}: No such file or directory'.format(dir))

else:
    last_dir_type = decode(tree.xpath('//INodeSection/inode[id="{}"]/type'.format(split_dir_id)))
    if last_dir_type == 'DIRECTORY':
        child_nodes_id = decode(tree.xpath('//INodeDirectorySection/directory[parent="{}"]/child'.format(split_dir_id)))
        child_nodes_id = [child_nodes_id] if isinstance(child_nodes_id, str) else child_nodes_id
    else:
        child_nodes_id = [split_dir_id]


    output = {}
    lens = {}
    print_keys = ['mode', 'replication', 'user_id', 'group_id', 'file_size', 'mtime', 'name']
    for key in print_keys:
        lens[key] = 0

    for node in child_nodes_id:
        output[node] = {}
        # type indicator
        node_type = decode(tree.xpath('//INodeSection/inode[id="{}"]/type'.format(node)))
        if node_type == "FILE":
            output[node]['mode'] = '-'
        else:
            output[node]['mode'] = 'd'
        # mode bits
        mode = decode(tree.xpath('//INodeSection/inode[id="{}"]/permission'.format(node)))
        output[node]['mode'] += translate_mode(mode.split(':')[-1])
        lens['mode'] = max(lens['mode'], len(output[node]['mode']))
        # number of replica
        replication = decode(tree.xpath('//INodeSection/inode[id="{}"]/replication'.format(node)))
        output[node]['replication'] = '-' if not replication else replication
        lens['replication'] = max(lens['replication'], len(output[node]['replication']))
        # user id
        output[node]['user_id'] = mode.split(':')[0]
        lens['user_id'] = max(lens['user_id'], len(output[node]['user_id']))
        # group id
        output[node]['group_id'] = mode.split(':')[1]
        lens['group_id'] = max(lens['group_id'], len(output[node]['group_id']))
        # file size
        file_size = decode(tree.xpath('//INodeSection/inode[id="{}"]//numBytes'.format(node)))
        if isinstance(file_size, list) and file_size:
            file_size = str(sum([int(x) for x in file_size]))
        output[node]['file_size'] = '0' if not file_size else file_size
        lens['file_size'] = max(lens['file_size'], len(output[node]['file_size']))
        # modification date, modification time
        mtime = decode(tree.xpath('//INodeSection/inode[id="{}"]//mtime'.format(node)))
        output[node]['mtime'] = datetime.datetime.fromtimestamp(int(mtime)/1e3).strftime('%Y-%m-%d %H:%M')
        lens['mtime'] = max(lens['mtime'], len(output[node]['mtime']))
        # file/directory name
        if last_dir_type == 'DIRECTORY':
            file_name = decode(tree.xpath('//INodeSection/inode[id="{}"]/name'.format(node)))
            output[node]['name'] = ('/').join(dir.split('/') + [file_name])
        else:
            output[node]['name'] = dir
        lens['name'] = max(lens['name'], len(output[node]['name']))


    if last_dir_type == 'DIRECTORY':
        print('Found {} items'.format(len(child_nodes_id)))

    if child_nodes_id:
        sorted_child_id = sorted(output.items(), key=lambda item: int(item[1]['file_size']))
        sorted_child_id = [x[0] for x in sorted_child_id]

        for node in sorted_child_id:
            print_line = ''
            for key in print_keys:
                print_line += output[node][key].rjust(lens[key]) + ' '
            print(print_line)