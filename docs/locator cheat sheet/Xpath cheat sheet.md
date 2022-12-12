### XPath cheat sheet


使用该[网站](https://demo.guru99.com/test/selenium-xpath.html)作为测试

| 表达式 | 样例 |描述|
| ----------- | :----------- |--------|
|Child|`//div[@class="g-grid"]/child::div`|取当前节点下的所有子节点|
|Parent|`//div[@class="g-grid"]/parent::*`|取当前节点的父节点|
|Descendant|`//div[@class="g-grid"]/descendant::div` |取当前节点下的所有`div`子孙节点|
|Ancestor|`//div[@class="g-grid"]/ancestor::div`|取当前节点的所有`div`祖先节点|
|following|`//div[@class="g-grid"]/following::div`|取当前节点后边的所有`div`节点|
|following-sibling|`//div[@class="g-grid"]/following-sibling::div`|取当前节点同一级别后边的所有`div`兄弟节点|
|preceding |`//div[@class="g-grid"]/preceding::div`|取当前节点前边的所有`div`节点|
|preceding-sibling |`//div[@class="g-grid"]/preceding-sibling::div`|取当前节点同一级别前边的所有`div`兄弟节点|
|Conatins|`//a[contains(text(), "R Programming")]`|取`text`包含`R Programming`的`a`标签|
|Starts-with| `//a[starts-with(text(), "R Programming")]`|取`text`以`R Programming`开头的`a`标签|
|Ends-with|`//a[ends-with(text(), "R Programming")]`|取`text`以`R Programming`结尾的`a`标签|
|And| `//input[@type = 'submit' and @value = 'LOGIN']`|取`type='submit'`并且`value='LOGIN'`的`input`标签, 等同于: `//input[@type = 'submit'][@value = 'LOGIN']`|
|Or|`//input[@type = 'submit' or @value = 'LOGIN']`|取`type='submit'`或者`value='LOGIN'`的`input`标签|
|Not|`//a[starts-with(text(), "R") and not(contains(text(),"Radio"))]`|取`text`以`R`开头但是又不包含`Radio`的`a`标签|
|Text|`//a[text()='R Programming']`|取文本等于`R Programming`的`a`标签, `text()`可以用`.`表示, 即`//a[.='R Programming']`|
|Position|`//div[@class="g-grid"][position()=2]` |取`class="g-grid"`位置为2的`div`标签|
||`//input[@checked]`|选择所有状态为`checked`的`input`标签|
||`//a[@disabled]`|选择所有状态为`disabled`的`a`标签|
||`//a[not(@disabled)]`|选择所有状态不为`disabled`的`a`标签|



#### 1. Child

当前节点: `//div[@class="g-grid"]` 

取当前节点下的所有子节点: `//div[@class="g-grid"]/child::div` 等同于 `//div[@class="g-grid"]/div`

取当前节点下的第N(N>=1)个子节点: `//div[@class="g-grid"]/child::div[N]` 等同于 `//div[@class="g-grid"]/div[N]`

取当前节点下的所有子孙节点: `//div[@class="g-grid"]//child::div` 等同于 `//div[@class="g-grid"]//div`

#### 2. Parent

当前节点: `//div[@class="g-grid"]` 

取当前节点的父节点: `//div[@class="g-grid"]/parent::div` 或者 `//div[@class="g-grid"]/parent::*`

#### 3. Descendant

当前节点: `//div[@class="g-grid"]` 

取当前节点下的所有`div`子孙节点: `//div[@class="g-grid"]/descendant::div` 等同于 `//div[@class="g-grid"]//div`

取当前节点下的第N(N>=1)个`div`子节点: `//div[@class="g-grid"]/descendant::div[N]`

取当前节点下的所有子孙节点: `//div[@class="g-grid"]/descendant::*` 等同于 `//div[@class="g-grid"]//*`

取当前节点下的所有`div`子孙节点并且包含当前节点: `//div[@class="g-grid"]/descendant-or-self::div` 


#### 4. Ancestor

当前节点: `//div[@class="g-grid"]` 

取当前节点的所有`div`祖先节点: `//div[@class="g-grid"]/ancestor::div`

取当前节点的第N(N>=1)个`div`祖先节点: `//div[@class="g-grid"]/ancestor::div[N]`

取当前节点的所有祖先节点: `//div[@class="g-grid"]/ancestor::*`

取当前节点的所有`div`祖先节点并且包含当前节点: `//div[@class="g-grid"]/ancestor-or-self::div` 

#### 5. Sibling

##### following

当前节点: `//div[@class="g-grid"]` 

取当前节点后边的所有`div`节点: `//div[@class="g-grid"]/following::div`

取当前节点后边的所有节点: `//div[@class="g-grid"]/following::*`


##### following-sibling

取当前节点同一级别后边的所有`div`兄弟节点: `//div[@class="g-grid"]/following-sibling::div`

取当前节点同一级别后边的所有兄弟节点: `//div[@class="g-grid"]/following-sibling::*`

##### preceding

取当前节点前边的所有`div`节点: `//div[@class="g-grid"]/preceding::div`

取当前节点前边的所有节点: `//div[@class="g-grid"]/preceding::*`

##### preceding-sibling 

取当前节点同一级别前边的所有`div`兄弟节点: `//div[@class="g-grid"]/preceding-sibling::div`

取当前节点同一级别前边的所有兄弟节点: `//div[@class="g-grid"]/preceding-sibling::*`

#### 6. Contains

取`text`包含`R Programming`的`a`标签: `//a[contains(text(), "R Programming")]`

取`title`包含`R Programming`的`a`标签: `//a[contains(@title, "R Programming")]`

#### 7. Starts-with

取`text`以`R Programming`开头的`a`标签: `//a[starts-with(text(), "R Programming")]`

取`title`以`R Programming`开头的`a`标签: `//a[starts-with(@title, "R Programming")]`

#### 8. Ends-with

取`text`以`R Programming`结尾的`a`标签: `//a[ends-with(text(), "R Programming")]`

取`title`以`R Programming`结尾的`a`标签: `//a[ends-with(@title, "R Programming")]`

`貌似已经不支持Ends-with了，使用会报错！`

#### 9. And 

取`type='submit'`并且`value='LOGIN'`的`input`标签: `//input[@type = 'submit' and @value = 'LOGIN']`

`可以和conatins、starts-with、ends-with、text一起使用`

#### 10. OR

取`type='submit'`或者`value='LOGIN'`的`input`标签: `//input[@type = 'submit' or @value = 'LOGIN']`

`可以和conatins、starts-with、ends-with、text一起使用`

#### 11. NOT

取`text`以`R`开头但是又不包含`Radio`的`a`标签: `//a[starts-with(text(), "R") and not(contains(text(),"Radio"))]`

#### 12. Text

取文本等于`R Programming`的`a`标签: `//a[text()='R Programming']`

取文本等于`R Programming`的`a`标签(取页面文本时会自动去除文本两端的空格):`//a[normalize-space(text())="R Programming"]`

#### 13. Position

取`class="g-grid"`位置为2的`div`标签: `//div[@class="g-grid"][position()=2]` 

取`class="g-grid"`位置大于1的`div`标签: `//div[@class="g-grid"][position()>1]`

#### 14. 其他

根据子节点的属性来获取父节点: `//div[@class="g-grid"]/div[div[@class="platform-content"]]`

取文本为`R Programming`的`a`标签的祖先`div`标签: `//div[.//a[text(）='R Programming']]`

取最后一个: `//div[@class="g-grid"][last()]`

取倒数第二个: `//div[@class="g-grid"][last()-1]`

取属性`data-val`的值大于1: `//div[@data-val>1]`

取`ul`下`li`数量大于2的`ul`: `//ul[count(li)>2]`

`//li[a="Java"]`

`//li[a[contains(., "Java")]]`

`//td[preceding-sibling::td="t"]`

`//td[preceding-sibling::td[contains(.,"t")]]`

按搜索结果的索引取值：`(//div[@class="g-grid"])[1]`


