import json

###################
## Helper functions
## short_name
# inputs:
#   s: a string of the format "firstname lastname"
# returns:
#   a string of the format "firstname first-initial-of-lname"
def shortname(s):
    ss = s.split()
    return '%s %s.' % (ss[0], ss[-1][0])

## Use this function between building blocks and tasks to make output easier
## to read
def gap(s=''):
    print '\n-----------' + s + '-----------'

## use this function to make more readable output of nested data structures
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

################
## Getting set up 
## This loads the Facebook group data as a list of dictionaries
posts = json.load(open('hw5feed.json'))['data']


## This extracts 3 dictionaries from the list of posts, which you will use
## as examples throughout the homework

mypost1 = posts[7]            # this is a post with one comment
mypost2 = posts[2]           # this is post without comments
mypost3 = posts[39]           # this is a post with likes and a comment

## Here is what a post dictionary looks like
print "==== example post ===="
print pretty(mypost1)

## posts is a list of dictionaries
print 'there are', len(posts), 'posts!'

####################
### Building Block 1
## extracting the name of a poster
gap('building block 1')

## write code that extracts and prints the data associated with the 'from'
## key in mypost1
#<your-code-here>
ks = mypost1.keys()
for k in ks:
    if k == "from":
        print mypost1[k]
## write code that extracts and prints the name of the user who posted mypost1
#<your-code-here>
for k in ks:
    if k == "from":
        data = mypost1[k]
        for i in data:
            if i == "name":
                print data[i]


## write a function postPoster() that extracts and returns the short name of
## the post from a post dictionary. 
## Use the shortname function within your function.
#<your-code-here>
def postPoster(d):
    for k in ks:
        if k == "from":
            data = d[k]
            for i in data:
                if i == "name":
                    return shortname(data[i])


## uncomment the following three lines to test
print postPoster(mypost1)
print postPoster(mypost2)
print postPoster(mypost3)

####################
### Building block 2
## extracting the number of comments for a post
gap('building block 2')

## some posts have comments
print mypost1['comments']

## other posts don't
## if you uncomment the following line, you'll get a
## key error -- the comments key isn't defined when
## there are no comments
#print mypost2['comments']

## here are what comment dictionaries look like
gap("a post's comment data structure")
print pretty(mypost1['comments'])

## this is how you get the number of comments from a comment dictionary
## if, and only if, that dictionary has comments (otherwise you get
## an error)
print "Comment count:", len(mypost1['comments']['data'])

## write a function called postCommentCount() that extracts and
## returns the number of comments from a post dictionary.
#<your-code-here>
def postCommentCount(d):
    if "comments" in d:
        return len(d['comments']['data'])
    else:
        return 0
            

## uncomment the following two lines of code. they should print 1 and 0
print postCommentCount(mypost1)
print postCommentCount(mypost2)

### Building block 3
# extracting like counts (this similar to comment counts, but
# the likes dictionary will be missing if there are no likes)

## here are what 'like' dictionaries contains
gap("a post's likes data structure")
print pretty(mypost3['likes'])

## but some posts don't have likes. You get an error when
## you uncomment the following line
#print pretty(mypost1['likes'])

## write code that gets the number of likes from mypost3
#<your-code-here>
print "Likes:", len(mypost3['likes']['data'])

## write a function called postLikeCount() that extracts and
## returns the number of likes from a post dictionary
## if the dictionary does not contain any likes, it should return 0
#<your-code-here>
def postLikeCount(d):
    if "likes" in d:
        return len(d['likes']['data'])
    else:
        return 0
    
## the following two lines should print 0 and 12 when uncommented
print postLikeCount(mypost1)
print postLikeCount(mypost3)

###########################
### Putting it all together
# Print out one line for each post in the dataset using the 3 functions
# that you have written(postPoster(), postCommentCount(), postLikeCount())
# Your output should look like:
#   Shortname posted to the group and received X comments and Y likes
#   with one line per post
gap("Task")
#<your-code-here>
for i in posts:
    print postPoster(i) + " posted to the group and received " + str(postCommentCount(i)) + " comments and " + str(postLikeCount(i)) + " likes."

