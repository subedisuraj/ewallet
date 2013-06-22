__author__ = 'Dell'

class Content:
    pagename = "pagename"
    content =""" pagecontent"""

    def __unicode__(self):
        return (self.pagename)


pwresetpage = Content()
contactpage = Content()
securitypage = Content()
faqpage = Content()
aboutpage = Content()


pwresetpage.pagename = "pwreset"
pwresetpage.content = """
<html>
<form method="POST">
    {% ifequal error 0 %}
Password changed successfully.
    {% endifequal %}
<label>
Current Password:
</label>
<input type = "password" name="cur_pass">
<br/>
    {% if errors.incorrect_pass %}
<span style="color: red; "> Current password in incorrect </span>
    {% endif %}
<label>
New Password:
</label>
<input type = "password" name="new_pass">
<br/>
    {% if errors.empty_error %}
<span style="color: red; "> This field is required </span>
    {% else %}
    {% if errors.limit_error %}
<span style="color: red; "> Passwords must contain 6 to 32 characters.   </span>
    {% endif %}

    {% endif %}
<label>
Confirm Password:
</label>
<input type = "password" name="conf_pass">
<br/>
<span style="color: red; "> * </span>
    {% if errors.mismatch_error %}
<span style="color: red; ">  Passwords didnt match. </span>
    {% endif %}
<input type = "submit" name = "change" value = "Change Password">


</form>
</html>
"""