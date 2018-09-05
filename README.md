# django-translation-tutorial

如何使用 Django 實作 translation  📝

* [Youtube Tutorial PART 1 - django-translation-tutorial](https://youtu.be/9zFCfnVgXjs)

* [Youtube Tutorial PART 2 - django-translation-tutorial](https://youtu.be/sz0cpt8I1fM)

* [Youtube Tutorial PART 3 - django-translation-tutorial](https://youtu.be/9njecageJvM)

## 簡介

本篇文章將介紹如何使用 Django 實作 translation ，我參考了 Django 官網的 [translation 文件](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/)，

並且紀錄了一些細節。如果你想用 Flask 實作的話，可參考我之前寫的文章 [Flask-Babel-example](https://github.com/twtrubiks/Flask-Babel-example)。

建議閱讀此篇文章之前，要對 docker 有一些基本的認識，如果你對 docker 不熟，建議可參考

[Docker 基本教學 - 從無到有 Docker-Beginners-Guide](https://github.com/twtrubiks/docker-tutorial)，為什麼會使用到 docker :question:

因為本身電腦是 windows，而 Django translation 需要安裝 `gettext`，我在 windows 中一直裝不起來，

所以最後果斷使用 docker :sweat_smile:

## 建立環境

我使用 docker 建立環境，先來看一下 [Dockerfile](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/Dockerfile)，

```text
FROM python:3.6.2
LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_tutorial
WORKDIR /docker_tutorial
COPY . /docker_tutorial/
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*
```

最重要的就是 `apt-get install -y gettext` 這個，我會用 docker 也是因為這個原因，windows 一直裝不起來阿:cry:

如果你是 Linux 或是 MAC，應該就不需要用 docker 了，本機理論上很好安裝。

接著執行以下指令建立環境，

```cmd
docker-compose build
```

再啟動環境 ( 其實也可以直接執行這個就好 )，

```cmd
docker-compose up
```

再來進入 docker 環境中 migrate，

```python
python manage.py migrate
```

如果上述不了解，可參考 [Docker 基本教學 - 從無到有 Docker-Beginners-Guide](https://github.com/twtrubiks/docker-tutorial)。

來看一下 [requirements.txt](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/requirements.txt)，這裡使用的是 `django==2.1.1`。

之前我寫的 django 教學文章，可參考 [Django 基本教學 - 從無到有 Django-Beginners-Guide 📝](https://github.com/twtrubiks/django-tutorial)，不過要注意的是，

這篇教學是 `django <= 2.0`，django 2 有機會我會再寫篇文章介紹。

由於 django 2 改動蠻大的，所以我在程式碼中，有些地方會增加註解，說明這段設定可以參考官網的哪部分文件。

## 教學

接下來就要教大家如何進行翻譯了，首先，先進入 [django_translation/settings.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/settings.py)，

找到 MIDDLEWARE，並且加入 `django.middleware.locale.LocaleMiddleware`，這邊要注意擺放的位置，

```python
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',

    # https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#how-django-discovers-language-preference
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    ...
]
```

一定要放在 `django.contrib.sessions.middleware.SessionMiddleware` 之後，

以及 `django.middleware.common.CommonMiddleware` 之前，原因如下，

下方為官方說明，

```text
It should come after SessionMiddleware, because LocaleMiddleware makes use of session
data. And it should come before CommonMiddleware because CommonMiddleware needs an
activated language in order to resolve the requested URL.
```

詳細的官方文件，可參考 [How Django discovers language preference](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#how-django-discovers-language-preference)。

設定 LOCALE_PATHS， 可參考 [setting-LOCALE_PATHS](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-LOCALE_PATHS)，

在 [django_translation/settings.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/settings.py) 中增加以下 code，這資料夾到時候會擺放翻譯的 `django.po` 以及 `django.mo` 檔案。

```python
LOCALE_PATHS =  [
    os.path.join(BASE_DIR, 'locale'),
]
```

在 [django_translation/settings.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/settings.py) 中的 LANGUAGE_CODE 為預設的語言

```python
LANGUAGE_CODE = 'en-us'
```

如果你不知道國家的 LANGUAGE_CODE，可到 [language-identifiers.html](http://www.i18nguy.com/unicode/language-identifiers.html) 查詢各國家的 LANGUAGE_CODE
。

接著在 [django_translation/settings.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/settings.py) 中設定可以顯示的語言清單，增加下列 code，

```python
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('en-us', _('English')),
    ('zh-hant', _('Traditional Chinese')),
    ('zh-cn', _('Simplified Chinese')),
]
```

`from django.utils.translation import gettext_lazy as _` 為翻譯，可參考 [standard-translation](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#standard-translation) ，

然後非常建議大家在看一下 [lazy-translation](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#lazy-translation) 這篇，了解哪時候要使用 `gettext_lazy` 以及為什麼要使用

`gettext_lazy`，通常是 defining models, forms and model forms 這些地方。

更多詳細設定，可參考
[How Django discovers language preference](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#how-django-discovers-language-preference)。

[django_translation/settings.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/settings.py) 的設定到這邊就算告一個段落了:relaxed:

接著設定 [django_translation/urls.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/urls.py) ，我們要增加 `path('i18n/', include('django.conf.urls.i18n'))`

到 urlpatterns 中，這個主要目的是 Activate this view，

以下為官方文件說明

```text
As a convenience, Django comes with a view, django.views.i18n.set_language(), that sets
a user’s language preference and redirects to a given URL or, by default, back to the
previous page.
Activate this view by adding the following line to your URLconf:
```

詳細可參考 [the-set-language-redirect-view](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#the-set-language-redirect-view)。

```python
urlpatterns = [
    # https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#the-set-language-redirect-view
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('tutorial/', include('tutorial.urls', namespace='tutorial' )),
]
```

接著設定 [tutorial/urls.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/urls.py)，設定好了之後，來看 [tutorial/views.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/views.py)，

讓我們來看在 view 中要怎麼實現翻譯， code 如下，

```python
from django.shortcuts import render
from django.utils.translation import gettext as _

# Create your views here.
def index(request):
    data = _('Hello')

    return render(request, 'tutorial/index.html', {
        "data" : data
    })
```

`_('Hello')` 這個就是翻譯。

( 像這邊就是使用 `from django.utils.translation import gettext as _`，而不是 `gettext_lazy`。)

有 view 之後，那接下來就是設定 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html)。

首先，我們先來設定可以切換語言的 select，可參考 [the-set-language-redirect-view](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#the-set-language-redirect-view)，

以下為官方範例 code，

```django
{% load i18n %}

<form action="{% url 'set_language' %}" method="post">{% csrf_token %}
    <input name="next" type="hidden" value="{{ redirect_to }}">
    <select name="language">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
        {% for language in languages %}
            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                {{ language.name_local }} ({{ language.code }})
            </option>
        {% endfor %}
    </select>
    <input type="submit" value="Go">
</form>
```

`{% load i18n %}` 很重要 ( 可參考 [internationalization-in-template-code](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#internationalization-in-template-code) 這邊的說明 )，記得要載入，

我自己有簡單的使用 bootstrap3，可參考 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html)，直接將翻譯文字顯示出來，

如下方 code，

```html
<div class="well well-sm">{{data}}</div>
```

到這邊，我們終於可以開始進行翻譯了:satisfied: ( 這邊我就只翻譯繁體，其他的以此類推 )。

首先需要先執行 [makemessages](https://docs.djangoproject.com/en/2.1/ref/django-admin/#makemessages) 指令，建立出 `django.po` 檔案，指令如下，

```cmd
django-admin makemessages --locale=zh_Hant
```

這段 code ，會去 scan 你的 code ，將需要翻譯的找出來。 ( 例如 `_('Hello')` 就會被 scan 出來 )。

![alt tag](https://i.imgur.com/X5FtFfc.png)

注意，如果出現如下圖錯誤，

![alt tag](https://i.imgur.com/HAdvlGe.png)

```text
CommandError: Can't find msguniq. Make sure you have GNU gettext tools 0.15 or newer installed.
```

這就是在 windows 上為什麼我用 docker 的原因，雖然網路上有人說 windows 可安裝 [gettext-iconv-windows](https://mlocati.github.io/articles/gettext-iconv-windows.html) 解決，

但我一直遇到問題，最後果斷使用 docker:smiley:

目錄中應該會有個 locale 的資料夾，因為我們在 LOCALE_PATHS 有設定，如果沒有請自行建立一個

( 當 django run 起來的時候應該就會自己建立了 )。

執行後會看到如下，產生了 zh_Hant 的 `django.po` 檔案，

![alt tag](https://i.imgur.com/TMnsHaD.png)

現在就是要對 `django.po` 進行翻譯，打開 `django.po`，你會發現 `'Hello'` 在裡面，

![alt tag](https://i.imgur.com/tbCKEEI.png)

將它翻譯後，再執行 compilemessages，可參考 [compilemessages](https://docs.djangoproject.com/en/2.1/ref/django-admin/#compilemessages)，指令如下

```python
django-admin compilemessages
```

![alt tag](https://i.imgur.com/Jk0TmrB.png)

執行後，如果沒任何錯誤訊息，就是成功 compilemessages，`django.mo` 就是 compilemessages 過後的檔案。

![alt tag](https://i.imgur.com/XrV9ah4.png)

接著我們到網頁上觀看 [http://127.0.0.1:8000/tutorial/](http://127.0.0.1:8000/tutorial/)，

英文

![alt tag](https://i.imgur.com/NuMoW6k.png)

中文

![alt tag](https://i.imgur.com/UPhJnuK.png)

我們也可以這樣寫，

```python
m=1
d= 20
output = _('Today is %(month)s / %(day)s.') % {'month': m, 'day': d}
```

[django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 如下，

![alt tag](https://i.imgur.com/ihIlByc.png)

這邊要提醒大家，假如你有做任何修改時，重新執行了 `django-admin makemessages --locale=zh_Hant` 時，

你可能會看到像上圖 A 的部份，就是你修改之前的東西會幫你註解起來，我建議把這個都刪除，也就是 A 的部份。

( 會請大家刪除的原因是，有時候它會導致你翻譯翻不出來，最後我是把那部份都刪除後，再執行  compilemessages 就正常了 )

![alt tag](https://i.imgur.com/qI3tY3W.png)

### contextual-markers

什麼時候會用到它呢 ? 在英文翻中文常常會有這種況狀，就是一個英文的詞，在中文有很多意思的時候。

舉個例子， blue 是 藍色 的意思，但 blue 也可以是 鬱悶 的意思，這時候，就需要使用 contextual-markers，

參考以下 code ( 更多說明請參考 [contextual-markers](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#contextual-markers) )，code 在 [tutorial/views.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/views.py)，

```python
...
from django.utils.translation import pgettext

# Create your views here.
def index(request):
    ...
    # Translators: contextual-markers
    p_blue_color = pgettext("color", "blue")
    # Translators: contextual-markers
    p_blue_mood = pgettext("mood", "blue")
    ...
    return render(request, 'tutorial/index.html', {
        ...
        "p_blue_color": p_blue_color,
        "p_blue_mood": p_blue_mood,
        ....
    })
```

然後如果們執行 `django-admin makemessages --locale=zh_Hant`，你會發現 [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 如下，

![alt tag](https://i.imgur.com/zvTbh4D.png)

你會發現它被拆成兩個，將對應要翻譯的內容填進去就可以了。另外注意一下這個註解，也就是

`# Translators: contextual-markers` 這個，如果你要在翻譯中註解，你可以在 python 中使用

`# Translators` key 開頭，這樣 [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 就會有註解，更多詳細介紹可參考 [comments-for-translators](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#comments-for-translators)。

翻譯完成後，再執行 compilemessages，

如果是在 html 中想要使用 contextual-markers，則必須使用以下 code，

```django
{# contextual-markers #}
<div class="well well-sm">{% trans "blue" context "color" %}</div>
<div class="well well-sm">{% trans "blue" context "mood" %}</div>
```

![alt tag](https://i.imgur.com/viDCMKi.png)

### pluralization

有時候我們會有單數和複數顯示不同的需求，這時候就可以使用
[pluralization](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#pluralization)，官方說明如下

```text
ngettext() takes three arguments: the singular translation string, the plural translation
string and the number of objects.
```

範例 code，code 在 [tutorial/views.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/views.py)，

```python
from django.utils.translation import ngettext
# pluralization
count = 2
pluralization = ngettext(
'There is %(count)d %(name)s object available.',
'There are %(count)d %(name)s objects available.',
count
) % {
    'count': count,
    'name':'test',
}
```

執行 makemessages，

![alt tag](https://i.imgur.com/AfoqZlv.png)

在 html 中，

```html
{# pluralization #}
<div class="well well-sm">{{pluralization}}</div>
```

![alt tag](https://i.imgur.com/naaDKpt.png)

你可以把 count 改成 `count = 1`，這樣就會變成單數了。

### Internationalization: in template code

接著來看在 template 中要如何進行翻譯，請參考 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html)，

```django
{% load i18n %}

{% comment %}Translators: Hello Django{% endcomment %}
<div class="well well-sm">{% trans "Hello Django" %}</div>

{# Translators: comment #}
<div class="well well-sm">{% trans "comment" %}</div>
```

上面提供了兩種的註解方式，詳細可參考 [comments-for-translators-in-templates](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#comments-for-translators-in-templates)。

`{% load i18n %}` 記得要載入，

接著執行 `django-admin makemessages --locale=zh_Hant` 產生  [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 檔案

![alt tag](https://i.imgur.com/D8Hj7RG.png)

註解也會產生在你的  [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 中，最後 compilemessages，

![alt tag](https://i.imgur.com/pGmmMaa.png)

另外還有一種是設定為變數，方法如下

```django
{# Translators: var #}
{% trans "This is the title" as the_title %}
<div class="well well-sm">{{ the_title }}</div>
```

剩下的部分和剛剛都一樣，這邊我就不再做一遍了。

接下來是可能有一種情況，例如，英文是顯示 `show Hello`，而中文要顯示 `哈摟顯示`，

這時候，我們就不能使用之前的 `{% trans "This is the title" %}` 的方法，因為中英的位置

不一樣，這時候，就必須使用 `Translators: "{% blocktrans %}....{% endblocktrans %}` 的方式，

下列為變數的方法，寫法有兩種，code 請參考 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html)，

```django
{# Translators: "{% blocktrans %}....{% endblocktrans %} #}
<div class="well well-sm">{%blocktrans with d=data %}show {{d}}{%endblocktrans%}</div>
<div class="well well-sm">{%blocktrans with data as d %}show {{d}}{%endblocktrans%}</div>
```

接著執行 `django-admin makemessages --locale=zh_Hant` 產生  [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 檔案，

![alt tag](https://i.imgur.com/1LpeUEk.png)

剩下的步驟這邊就省略了:relaxed:前面都說很多次了。

再來說一下 `trimmed option`，

有時候，我們希望經過 `django-admin makemessages --locale=zh_Hant` 產生  [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 的檔案不要有換行

字元 `\n` 這類的，這時候，就可以使用  trimmed 這個 option。

( 有時候 `\n` 這類的字元甚至會導致翻譯錯誤，所以建議能加 trimmed 就加吧 )

```django
{% blocktrans trimmed %}
First sentence.
Second sentence.
{% endblocktrans %}
```

再來說一下另一個 `noop option`，官方說明如下，

```text
If the noop option is present, variable lookup still takes place but the translation is
skipped. This is useful when “stubbing out” content that will require translation in
the future:
```

如果加上這個 `noop option`，它將不會被翻譯，經過 `django-admin makemessages --locale=zh_Hant`

產生  [django.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/django.po) 的檔案中，還是會有翻譯的內容，但不會被翻譯出來( skipped )，也就是說，可以使用在未來

會翻譯，但目前還不需要的情境下，

```django
{# Translators: noop #}
<div class="well well-sm">{% trans "myvar" noop  %}</div>
```

### Internationalization: in JavaScript code

* [Youtube Tutorial PART 3 - django-translation-tutorial](https://youtu.be/9njecageJvM)

一定會有人問，那如果我是透過 javascript ，有辦法進行翻譯嗎:question:

是可以的:satisfied:這邊就來教大家如何設定，

先到 [django_translation/urls.py](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/django_translation/urls.py) 設定 [The JavaScriptCatalog view](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#module-django.views.i18n)，

```python
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    ....
    #https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#module-django.views.i18n
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    ...
]
```

接著在 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html) 中新增以下 code，

```django
{# Using the JavaScript translation catalog #}
{# https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#using-the-javascript-translation-catalog #}
<script type="text/javascript" src="{% url 'javascript-catalog' %}"></script>
```

更多詳細介紹可參考官方文件 [using-the-javascript-translation-catalog](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#using-the-javascript-translation-catalog)。

接下來請注意，請 **新增一個 js 檔案** ，不能直接將 js 寫在 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html)  中，

會抓不到，所以我們新增一個 [tutorial/static/js/index.js](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/static/js/index.js) 檔案，並且在裡面填入以下 code，

使用方法也很簡單，和在 python 翻譯的時候差不多，考以直接使用 [gettext](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#gettext)，

```javascript
var data = gettext('this is to be translated')
document.write( '<div class="well well-sm">'+ data + '</div>');
```

之後再回到 [tutorial/templates/tutorial/index.html](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/tutorial/templates/tutorial/index.html) 中 import 它，

```django
{% load static %}
<script type="text/javascript" src="{% static "tutorial/index.js" %}"></script>
```

接著我們要建立 [djangojs.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/djangojs.po)，指令有點不一樣，

```python
django-admin makemessages -d djangojs -l zh_Hant
```

![alt tag](https://i.imgur.com/NAN8l3r.png)

執行後你會發現多出 [djangojs.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/djangojs.po)，

![alt tag](https://i.imgur.com/nsgq8n8.png)

[djangojs.po](https://github.com/twtrubiks/django-translation-tutorial/blob/master/django_translation/locale/zh_Hant/LC_MESSAGES/djangojs.po) 的內容如下，這邊我們成功的抓到 js 裡面的翻譯，

![alt tag](https://i.imgur.com/BOAjA15.png)

更多詳細可參考 [Creating message files from JavaScript source code](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#creating-message-files-from-javascript-source-code)，

接著執行 compilemessages，指令則是一樣的，`django-admin compilemessages`

![alt tag](https://i.imgur.com/bs2L6Pc.png)

最後再到網頁上觀看 [http://127.0.0.1:8000/tutorial/](http://127.0.0.1:8000/tutorial/)，js 也成功翻譯了:smiley:

![alt tag](https://i.imgur.com/QbXvtuT.png)

## 後記：

這次一不小心寫了好多，很多地方基本上我都有在 code 的部分放上註解以及官方的參考網址，

整體來說，我覺得 [django-translation](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/) 蠻完善的，連 js 也整合了進來，這次就介紹到這邊，謝謝大家:heart_eyes:

## 執行環境

* Python 3.6.2
* windows 10

## Reference

* [django-translation](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/)

* [django-bootstrap3](https://github.com/dyve/django-bootstrap3)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license
