#-!- coding=utf-8 -!-

def __node_get_data( node ) :
    """
    get data from node
    """
    return node[1]

def __node_set_data( node, data ) :
    """
    set data to node
    """
    node[1] = data

def __node_seek_node( node, code ) :
    """
    seek node with code, only seek one layer
    return list index of node
    if not find, return -1
    """
    index = 0
    flag = False
    while ( not flag ) and index < len( node[2] ) :
        sub_node = node[2][index]
        if sub_node[0] == code :
            flag = True
        else :
            index = index + 1
    if flag == False :
        index = -1
    return index

def __node_seek_path( node, path ) :
    """
    seek path under node
    path is some code like "944"
    each code of path is "9", "4", "4"
    return seeked_path and node
    """
    seeked_path = ""
    index = 0
    flag = True
    while flag and index < len( path ) :
        code = path[index]
        seek_index = __node_seek_node( node, code )
        if seek_index < 0 :
            flag = False
        else :
            node = node[2][seek_index]
            seeked_path = seeked_path + code
        index = index + 1
    return seeked_path, node

def __node_seek_path_ex( node ) :
    """
    seek path under a node
    this function use A* seek
    will keep seek until get the node/nodes have data
    path is some code like "944"
    each code of path is "9", "4", "4"
    return list of seeked_path and node
    """
    result = []
    node_list = [ node ]
    path_list = [ "" ]
    node_stack = []
    path_stack = []
    while len( node_list ) > 0 and len( result ) < 1 :
        for i in range( len( node_list ) ) :
            node = node_list[i]
            path = path_list[i]
            if node[1] :
                result.append( [ path, node ] )
            else :
                if len( result ) < 1 :
                    for sub_node in node[2] :
                        node_stack.append( sub_node )
                        path_stack.append( path + sub_node[0] )
        node_list = node_stack
        path_list = path_stack
        node_stack = []
        path_stack = []
    return result

def __node_add_path( node, path ) :
    """
    add a new node in path under node
    path is some code like "944"
    each code of path is "9", "4", "4"
    if path existed, do nothing
    return node under path
    """
    for code in path :
        index = __node_seek_node( node, code )
        if index < 0 :
            node[2].append( [ code, None, [] ] )
            node = node[2][-1]
        else :
            node = node[2][index]
    return node


node_add_path = __node_add_path
node_seek_path = __node_seek_path
node_seek_path_ex = __node_seek_path_ex

get_data = __node_get_data
set_data = __node_set_data

class CodeMap() :
    def __init__( self ) :
        """
        node in code_map contain 3 element :
        1. code - a string
        2. data - any data
        3. child_node_list - like it's name
        """
        self.entry = [ "", None, [] ]

    def add_path( self, path ) :
        """
        add a new node in path
        path is some code like "944"
        each code of path is "9", "4", "4"
        if path existed, do nothing
        return node under path
        """
        return node_add_path( self.entry, path )

    def seek( self, path ) :
        """
        seek path
        path is some code like "944"
        each code of path is "9", "4", "4"
        return seeked_path and node
        """
        return node_seek_path( self.entry, path )

    def power_seek( self, path ) :
        """
        seek path
        path is some code like "944"
        each code of path is "9", "4", "4"
        this function use A* seek
        will keep seek until get the node/nodes have data
        return seeked_path and node
        """
        seeked_path, node = node_seek_path( self.entry, path )
        if seeked_path == path :
            if get_data( node ) :
                flag = True
                result = [ [ seeked_path, node ] ]
            else :
                flag = False
                result = node_seek_path_ex( node )
                for item in result :
                    item[0] = seeked_path + item[0]
        else :
            flag = False
            result = None
        return flag, result

