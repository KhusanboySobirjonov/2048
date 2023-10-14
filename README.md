# 2048
Game 2048

<img src="2048_logo.png">

The modules in the requirements.txt file are installed by issuing the following command in the terminal.

<pre>pip install -r requirements.txt</pre>

The remaining modules are standard python modules. Run the main.py file to run the game.

Use the pyinstaller module to convert the game to .exe format. And run the following command in the terminal :

<pre>pyinstaller main.py --onefile -w</pre>


You can perform the following modifications to perform additional customization work in the game.

<code>self.__size</code> - creating an <code>NxN</code> board. The minimum value of <code>N</code> should be 4.

<code>self.__dict_color</code> - list of colors used in numbers. You can change it with your favorite colors.



Colors used in numbers :

<code>#cdc1b5</code> - <span style="color:#cdc1b5">0</span>
 
<code>#eee4da</code> - <span style="color:#eee4da">2</span>

<code>#ece0c8</code> - <span style="color:#ece0c8">4</span>

<code>#f8ba05</code> - <span style="color:#f8ba05">8</span>

<code>#fb9b00</code> - <span style="color:#fb9b00">16</span>

<code>#fe5404</code> - <span style="color:#fe5404">32</span>

<code>#fc290c</code> - <span style="color:#fc290c">64</span>

<code>#a9174b</code> - <span style="color:#a9174b">128</span>

<code>#8701b1</code> - <span style="color:#8701b1">256</span>

<code>#158dc7</code> - <span style="color:#158dc7">512</span>

<code>#0844fc</code> - <span style="color:#0844fc">1024</span>

<code>#67b131</code> - <span style="color:#67b131">2048</span>

<code>#d2e929</code> - <span style="color:#d2e929">4096</span>

Leave a comment if you have ideas for additional colors. For numbers after 4096.

