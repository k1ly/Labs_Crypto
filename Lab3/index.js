const {app, BrowserWindow} = require('electron');

app.whenReady().then(() => {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        autoHideMenuBar: true
    });
    win.loadFile('index.html');
})