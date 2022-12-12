import configparser
import os
import datetime
import praw
import markdown
import dominate
import PySimpleGUI as sg

from pathvalidate import sanitize_filename
from mdutils.mdutils import MdUtils
from dominate.tags import *
from dominate.util import raw

class RedditPost:
    def __init__(self) -> None:
        self.title = ""
        self.url = ""
        self.author_name = ""
        self.author_profile = ""
        self.selftext = ""
        self.comments = []
        self.sub_name = ""
        self.sub_url = ""
        self.timestamp = ""
    # ---
# ---

# Gets SVG code for the icons.
def get_icons_svg(type="user"):
    
    svg_tag = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                  <path fill="currentColor" 
                  d="M21.41 11.58L12.41 2.58A2 2 0 0 0 11 2H4A2 2 0 0 0 2 4V11A2 
                  2 0 0 0 2.59 12.42L11.59 21.42A2 2 0 0 0 13 22A2 2 0 0 0 14.41 
                  21.41L21.41 14.41A2 2 0 0 0 22 13A2 2 0 0 0 21.41 11.58M13 20L4 
                  11V4H11L20 13M6.5 5A1.5 1.5 0 1 1 5 6.5A1.5 1.5 0 0 1 6.5 5Z" />
                 </svg>"""

    svg_user = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                   <path fill="currentColor" 
                   d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 
                   12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
                  </svg>"""

    svg_timer_sand = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                         <path fill="currentColor" d="M6,2H18V8H18V8L14,12L18,
                         16V16H18V22H6V16H6V16L10,12L6,8V8H6V2M16,16.5L12,12.5L8,
                         16.5V20H16V16.5M12,11.5L16,7.5V4H8V7.5L12,11.5M10,
                         6H14V6.75L12,8.75L10,6.75V6Z" />
                        </svg>"""

    svg_comment_user = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M9,22A1,1 0 0,1 8,21V18H4A2,
                            2 0 0,1 2,16V4C2,2.89 2.9,2 4,2H20A2,2 0 0,1 22,4V16A2,2 0 0,
                            1 20,18H13.9L10.2,21.71C10,21.9 9.75,22 9.5,22V22H9M10,
                            16V19.08L13.08,16H20V4H4V16H10M16,14H8V13C8,11.67 10.67,11 12,
                            11C13.33,11 16,11.67 16,13V14M12,6A2,2 0 0,1 14,8A2,2 0 0,1 12,
                            10A2,2 0 0,1 10,8A2,2 0 0,1 12,6Z" />
                          </svg>"""

    svg_reddit = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                      <path fill="currentColor" d="M14.5 15.41C14.58 15.5 14.58 
                      15.69 14.5 15.8C13.77 16.5 12.41 16.56 12 16.56C11.61 16.56 
                      10.25 16.5 9.54 15.8C9.44 15.69 9.44 15.5 9.54 15.41C9.65 
                      15.31 9.82 15.31 9.92 15.41C10.38 15.87 11.33 16 12 16C12.69 
                      16 13.66 15.87 14.1 15.41C14.21 15.31 14.38 15.31 14.5 15.41M10.75 
                      13.04C10.75 12.47 10.28 12 9.71 12C9.14 12 8.67 12.47 8.67 13.04C8.67 
                      13.61 9.14 14.09 9.71 14.08C10.28 14.08 10.75 13.61 10.75 13.04M14.29 
                      12C13.72 12 13.25 12.5 13.25 13.05S13.72 14.09 14.29 14.09C14.86 14.09 
                      15.33 13.61 15.33 13.05C15.33 12.5 14.86 12 14.29 12M22 12C22 17.5 17.5 
                      22 12 22S2 17.5 2 12C2 6.5 6.5 2 12 2S22 6.5 22 12M18.67 12C18.67 11.19 
                      18 10.54 17.22 10.54C16.82 10.54 16.46 10.7 16.2 10.95C15.2 10.23 13.83 
                      9.77 12.3 9.71L12.97 6.58L15.14 7.05C15.16 7.6 15.62 8.04 16.18 8.04C16.75 
                      8.04 17.22 7.57 17.22 7C17.22 6.43 16.75 5.96 16.18 5.96C15.77 5.96 15.41 
                      6.2 15.25 6.55L12.82 6.03C12.75 6 12.68 6.03 12.63 6.07C12.57 6.11 12.54 
                      6.17 12.53 6.24L11.79 9.72C10.24 9.77 8.84 10.23 7.82 10.96C7.56 10.71 
                      7.2 10.56 6.81 10.56C6 10.56 5.35 11.21 5.35 12C5.35 12.61 5.71 13.11 6.21 
                      13.34C6.19 13.5 6.18 13.62 6.18 13.78C6.18 16 8.79 17.85 12 17.85C15.23 
                      17.85 17.85 16.03 17.85 13.78C17.85 13.64 17.84 13.5 17.81 13.34C18.31 
                      13.11 18.67 12.6 18.67 12Z" />
                    </svg>
                    """
    
    svg_calendar_clock = """<svg style="width:24px;height:24px" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M15,13H16.5V15.82L18.94,17.23L18.19,
                                18.53L15,16.69V13M19,8H5V19H9.67C9.24,18.09 9,17.07 9,16A7,7 0 0,1 
                                16,9C17.07,9 18.09,9.24 19,9.67V8M5,21C3.89,21 3,20.1 3,19V5C3,3.89 
                                3.89,3 5,3H6V1H8V3H16V1H18V3H19A2,2 0 0,1 21,5V11.1C22.24,12.36 23,
                                14.09 23,16A7,7 0 0,1 16,23C14.09,23 12.36,22.24 11.1,21H5M16,
                                11.15A4.85,4.85 0 0,0 11.15,16C11.15,18.68 13.32,20.85 16,
                                20.85A4.85,4.85 0 0,0 20.85,16C20.85,13.32 18.68,11.15 16,11.15Z" />
                            </svg>"""

    if type == "user":
        return svg_user
    elif type == "tag":
        return svg_tag
    elif type == "timer":
        return svg_timer_sand
    elif type == "comment_user":
        return svg_comment_user
    elif type == "reddit":
        return svg_reddit
    elif type == "calendar_clock":
        return svg_calendar_clock
# ---

# Gets comment details.
def get_comment_details(comment, depth=0):
    """Generate comment bodies and depths."""
    comment_author_name = ""
    comment_author_profile = ""

    if comment.author == None:
        comment_author_name = "[deleted]"
        comment_author_profile = "#"
    else:
        comment_author_name = comment.author.name
        comment_author_profile = "https://www.reddit.com/user/" + comment_author_name

    yield comment_author_name, comment_author_profile, comment.created, comment.body, depth
    for reply in comment.replies:
        yield from get_comment_details(reply, depth + 1)
# ---

# Gets all comments of the post.
def get_post_comments(post, more_limit=32):
    """Get a list of (body, depth) pairs for the comments in the post."""

    comments = []
    post.comments.replace_more(limit=more_limit)
    
    for top_level in post.comments:
        comments.extend(get_comment_details(top_level))

    return comments
# ---

# Gets the date of submission post.
def get_post_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)
# ---

# Gets the reddit instance.
def get_reddit_instance():
    reddit_client_id = get_config_value("reddit", "client_id")
    reddit_client_secret = get_config_value("reddit", "client_secret")
    reddit_user_agent = get_config_value("reddit", "user_agent")

    if is_string_empty(reddit_client_id) == True or is_string_empty(reddit_client_secret) == True or is_string_empty(reddit_user_agent) == True:
        return None

    return praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
# ---

# Creates a detailed post object.
def get_post_details(post_url, submission):
    reddit_post = RedditPost()

    post_author_name = ""
    if submission.author == None:
        post_author_name = "[deleted]"
        post_author_profile = "#"
    else:
        post_author_name = submission.author.name
        post_author_profile = "https://www.reddit.com/user/" + submission.author.name

    submission.comments.replace_more(limit=0)
    if submission.num_comments > 0:
        all_comments = get_post_comments(submission)

    reddit_post.title = submission.title
    reddit_post.url = post_url
    reddit_post.author_name = post_author_name
    reddit_post.author_profile = post_author_profile
    reddit_post.selftext = submission.selftext
    reddit_post.comments = all_comments
    reddit_post.sub_name = "r/" + str(submission.subreddit.display_name)
    reddit_post.sub_url = "https://www.reddit.com/r/" + submission.subreddit.display_name
    reddit_post.timestamp = str(get_post_date(submission))

    return reddit_post
# ---

# Processes the url.
def process_url(post_url):
    """Process the post url"""

    # An example url to a reddit post
    # post_url = "https://www.reddit.com/r/redditdev/comments/5dfzw0/praw4_getting_all_commentsreplies_of_a_tree/"

    reddit = get_reddit_instance()

    if reddit == None:
        return

    submission = reddit.submission(url=post_url)

    reddit_post = get_post_details(post_url, submission)

    exported_file_name = make_html(reddit_post)

    return exported_file_name
# ---

# Gets the window layout.
def get_window_layout():
    # Layout for gui window.
    layout = [  [sg.Text("Links to reddit posts")],
                [sg.Multiline(key="-INPUTURLS-", tooltip=" One link per line ", size=(73,10), autoscroll=True)], 
                [sg.Push(), sg.Button("Go"), sg.Button("Cancel")],
                [sg.Multiline("", size=(85,3), key="-MESSAGE-", 
                 disabled=True, autoscroll=True, background_color="#eee", font=("Consolas", 8))] ]

    return layout
# ---

# Gets value from the config file.
def get_config_value(section="", option=""):

    config = configparser.ConfigParser()
    config.read("config.ini")

    if config.has_option(section, option):
        return config.get(section, option)
    else:
        return None
# ---

# Checks if string is empty and returns true/false.
def is_string_empty(str=""):
    if str == None:
        return True
    if str == "":
        return True
    
    return False
# ---

# Makes config and saves to the disk.
def make_config():
    config = configparser.ConfigParser()

    config.add_section("reddit")
    config.set("reddit", "client_id", "")
    config.set("reddit", "client_secret", "")
    config.set("reddit", "user_agent", "")

    config.add_section("options")
    config.set("options", "export_html", "no")
    config.set("options", "dark_mode", "no")

    try:
        with open("config.ini", "w") as configfile:
            config.write(configfile)
    except IOError as eIOError:
        print("IOError: " + str(eIOError))
# ---

# Makes and exports html file.
def make_html(reddit_post:RedditPost):
    h_name = sanitize_filename("[reddit] " + reddit_post.author_name + " - " + reddit_post.title)
    h_name = h_name[0:128] # keep filename at the maximum length of 128
    h_ext = ".html"

    d_css_file = "styles.css"
    d_css = ""
    with open(d_css_file, "r") as f:
        d_css = f.read()

    d = dominate.document(title=h_name)
    with d.head:
        style(raw(d_css), pretty=True)

    # toggle button
    div_toggle = div(_class="toggle-button")
    div_toggle.add(input_(type="checkbox", _class="checkbox", id="chk"))
    label_toggle = label(_for="chk", _class="label")
    label_toggle.add(div(_class="ball"))
    div_toggle.add(label_toggle)

    d += div_toggle

    # title
    div_title = div(_class="title")
    div_title.add(h1(a(reddit_post.title, href=reddit_post.url)))
    d += div_title

    div_details = div(_class="details")

    # author
    div_author = a(href=reddit_post.author_profile, _class="item", target="_blank")
    div_author += span(raw(get_icons_svg("user")), _class="item-icon")
    div_author += span(reddit_post.author_name, _class="item-text")

    # subreddit
    div_subreddit = a(href=reddit_post.sub_url, _class="item", target="_blank")
    div_subreddit += span(raw(get_icons_svg("reddit")), _class="item-icon")
    div_subreddit += span(reddit_post.sub_name, _class="item-text")

    # timer
    div_timestamp = span(_class="item")
    div_timestamp += span(raw(get_icons_svg("calendar_clock")), _class="item-icon")
    div_timestamp += span(reddit_post.timestamp, _class="item-text")

    div_details.add(div_author)
    div_details.add(div_subreddit)
    div_details.add(div_timestamp)

    # details
    d += div_details

    # content
    div_selftext = div(_class="selftext")
    div_selftext.add(raw(markdown.markdown(reddit_post.selftext)))

    d += div_selftext

    div_comments = div(_class="comments")
    div_comments.add(h3("Comments", _class="comments-main-header"))

    # comments
    for comment in reddit_post.comments:

        div_comment_details = div(_class="details")
        
        comment_author_name = comment[0]
        comment_author_profile = comment[1]
        comment_timestamp = comment[2]
        comment_body = comment[3]
        comment_depth = comment[4]

        comment_created_at = str(datetime.datetime.fromtimestamp(comment_timestamp))

        comment_author_op = ""
        if reddit_post.author_name != "[deleted]":
            if reddit_post.author_name == comment_author_name:
                comment_author_op = " (OP)"
            else:
                comment_author_op = ""
        else:
            comment_author_op = ""

        div_comment_author = span(a(comment_author_name + comment_author_op, href=comment_author_profile, target="_blank"), _class="comment-author")
        div_comment_timestamp = span(comment_created_at, _class="comment-timestamp")

        div_comment_details.add(div_comment_author)
        div_comment_details.add(div_comment_timestamp)

        div_comment_text = div(raw(markdown.markdown(comment_body)))

        comment_blockquote_prefix = "<blockquote>" * comment_depth
        comment_blockquote_postfix = "</blockquote>" * comment_depth

        if comment_depth == 0:
            div_comments.add(hr())

        div_comments.add(raw(comment_blockquote_prefix))
        div_comments.add(div_comment_details)
        div_comments.add(div_comment_text)
        div_comments.add(raw(comment_blockquote_postfix))

    # Add all comments
    d += div_comments

    # Add a horizontal line to indicate a visible end of file.
    d += hr()

    # script
    d_script_file = "script.js"
    d_script = ""
    with open(d_script_file, "r") as f:
        d_script = f.read()

    d += script(raw(d_script))

    with open(os.path.join("exported", h_name + h_ext), "w", encoding="utf-8") as f:
        f.write(d.render(pretty=True))

    return h_name
# ---

# Main.
def main():

    # Create config file if it doesn't exist.
    if os.path.exists("config.ini") == False:
        make_config()

    if os.path.exists("exported") == False:
        os.mkdir("exported")

    post_urls_array = []

    # Create the window.
    window = sg.Window("Download reddit post", get_window_layout(), finalize=True)
    message = window["-MESSAGE-"]
    message.update("Ready...")

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == "Cancel": 
            # if user closes window or clicks cancel.
            break
        
        post_urls_array = values["-INPUTURLS-"].splitlines()

        if len(post_urls_array) == 0:
            window["-MESSAGE-"].update("Enter link(s) to reddit posts")
        else:
            try:
                for i in range(0, len(post_urls_array)):
                    file_name = process_url(post_urls_array[i])
                    if file_name == None:
                        message.update(message.get() + "\nUnexpected error. Please check config.ini for valid values.")
                    else:
                        message.update(message.get() + "\nExported: " + file_name)
            except IndexError as eIndex:
                print("IndexError: " + str(eIndex))
                message.update("IndexError: " + str(eIndex))
            except TypeError as eType: 
                print("TypeError: " + str(eType))
                message.update("TypeError: " + str(eType))
                sg.popup_error_with_traceback(f'An error happened.  Here is the info:', eType)
            except UnicodeEncodeError as eUnicodeEncode:
                print("UnicodeEncodeError: " + str(eUnicodeEncode))
                message.update("UnicodeEncodeError: " + str(eUnicodeEncode))
            except AttributeError as eAttributeError:
                print("AttributeError: " + str(eAttributeError))
                message.update("AttributeError: " + str(eAttributeError))
            except Exception as eXception:
                print("Exception: ", str(eXception))
                message.update("Exception: ", str(eXception))
                sg.popup_error_with_traceback(f'An error happened.  Here is the info:', eXception)

    # Close the window once loop is broken.
    window.close()
# ---

# Main program starts.
if __name__ == "__main__":
    main()
# ===