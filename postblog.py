python << EOF
# Post to Blog
import re
import vim
import xmlrpclib

blog_username = 'username'
blog_password = 'password'
blog_url = 'http://link.to.host/xmlrpc.php'

def post_blog():
    strid = ''
    offsetline = 0

    if vim.current.buffer[0].find('StrID:') != -1:
        strid = vim.current.buffer[0].split(':')[1]
        offsetline = 1 
       
    title = vim.current.buffer[offsetline + 0]
    tags = vim.current.buffer[offsetline + 1]
    text = '\n'.join(vim.current.buffer[offsetline + 2:])

    # If we find [tags] and [/tags] we don't need to include the [tags]s
    if tags.find('[tags]') == -1 and tags.find('[/tags]') == -1
        tags = '[tags]' + tags + '[/tags]\n'

    content = tags + text

    wp = xmlrpclib.ServerProxy(blog_url)
    post = { 
        'title': title,
        'description': content 
    }

    if strid == '':
        strid = wp.metaWeblog.newPost('', blog_username, 
            blog_password, post, 1)

        vim.current.buffer.append('\n')
        vim.current.buffer[:] = ['StrID:' + strid] + \
            [i for i in vim.current.buffer[:]]
    else:
        wp.metaWeblog.editPost(strid, blog_username,
            blog_password, post, 1)

    vim.command('set nomodified') 

def get_post():
    pass
EOF
