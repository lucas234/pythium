#### Css cheat sheet


使用该[网站](https://demo.guru99.com/test/selenium-xpath.html)作为测试

| 表达式 | 样例 |描述|
| ----------- | :----------- |--------|
|`#id`|`#java_technologies`|取`id='java_technologies'`的节点(多个时只选择第一个)|
|`tagName#id`|`ul#java_technologies`|取所有`id='java_technologies'`的ul节点(选择多个)｜
|`.class`|`.menu`|取`class='menu'`的所有节点(选择多个)
|`.class1.class2`|`.col-md-2.header-section`|取`class='col-md-2 header-section'`的节点|
|`tagName.class`|`ul.menu`|取`class='menu'`的所有ul节点(选择多个)
|`[attribute]`|`[id]`|取所有带有`id`的节点|
|`tagName[attribute]`|`ul[id]`|取所有带有`id`的`ul`节点|
|`[attribute=value]`|`[id="java_technologies"]`|取`id="java_technologies"`的节点|
|`tagName[attribute=value]`|`ul[id="java_technologies"]`|取`id="java_technologies"`的ul节点|
|`elemen­t1>­ele­ment2`|`div.logo > a`|取`class="logo"`的div标签直系`孩子a`节点|
|`element1 element2`|`div.logo a`|取`class="logo"`的div标签`子孙a`节点|
|`element1~element2`|`ul.menu ~ p`|取`class="menu"`的ul标签的`相邻`节点|
|`element1+element2`|`ul.menu + p`|取`class="menu"`的ul标签的`相邻(直接跟在后边的)`节点|
|`starts-with`:`[attribute^=value]`|`[id^="java_"]`|取`id`以`java_`开头的|
|`ends-with`:`[attribute$=value]`|`[id$="technologies"]`|取`id`以`technologies`结尾的|
|`contains子串`:`[attribute*=value]`|`[id*="technologies"]`|取`id`包含`technologies`的|
|`contains 单词`:`[attribute~=value]`|`[id~="technologies"]`|取`id`包含单词`technologies`的(`value必须是以空格隔开中的一个`)|
|`tagName:contains(text)`|`a:contains("BigData")`|取文本包含`BigData`的`a`标签|
|`or`|`[type="submit"],[name="btnLogin"]`|取`type="submit"`或者`name="btnLogin"`的节点|
|`and`|`[type="submit"][name="btnLogin"]`|取`type="submit"`和`name="btnLogin"`的节点|
|`:not(.class-name)`|`[class*="top"]:not(.row)`|取`class`包含`top`且`class`不等于`row`的|
|`:first-of-type`|`ul.nav.navbar-nav>li:first-of-type`|取第一个`li`|
|`:last-of-type`|`ul.nav.navbar-nav>li:last-of-type`|取最后一个`li`|
|`:n­th-­of-­type(N)`|`ul.nav.navbar-nav>li:nth-of-type(2)`|取第二个`li`|
|`:n­th-­last-of-­type(N)`|`ul.nav.navbar-nav>li:nth-last-of-type(2)`|取倒数第二个`li`|
|`:frst-child`|`ul.nav.navbar-nav>li:first-child`|取第一个`li`|
|`:last-child`|`ul.nav.navbar-nav>li:last-child`|取最后一个`li`|
|`:nth-c­hild(N)`|`ul.nav.navbar-nav>li:nth-child(2)`|取第二个`li`|
|`:nth-last-child(N)`|`.nav.navbar-nav>li:nth-last-child(3)`|取倒数第三个`li`|
|`a:link`|`a:link`|获取所有link|
|`a:visited`|`a:visited`|获取所有查看过的`link`|
|`input:disabled`|`input:disabled`|所有`disabled`的`input`|
|`input:active`|`input:active`|所有`active`的`input`|
|`input:checked`|`input:checked`|获取选中的`checkbox`|
|`input:enabled`|`input:enabled`|所有`enabled`的`input`|
|`input:read-only`|`input:read-only`|带有`read-only`属性的`input`|
|`input:required`|`input:required`|带有`required`属性的`input`|
|`button:enabled`|`button:enabled`|获取`enabled`的`button`|
|`button:disabled`|`button:disabled`|获取`disabled`的`button`|





