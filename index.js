const { app, BrowserWindow, Tray, Menu, Notification } = require('electron');
const path = require('path');

let tray = null;
let mainWindow = null;

// const DELAY = 20 * 60 * 1000;
// const DURATION = 20 * 1000;

const DELAY = 30 * 1000;
const DURATION = 2 * 1000;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        fullscreen: true,
        frame: false,
        resizable: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    mainWindow.loadFile('index.html');

    // mainWindow.on('close', (event) => {
    //     event.preventDefault();
    // });

    setTimeout(() => {
        mainWindow.close();
    }, DURATION);
}

function createTray() {
    tray = new Tray(path.join(__dirname, 'icon.png'));
    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Quit',
            click: () => {
                app.quit();
            }
        }
    ]);
    tray.setToolTip('Eye Health Reminder');
    tray.setContextMenu(contextMenu);
}

function triggerPopup() {
    if (mainWindow) {
        mainWindow.focus();
    } else {
        createWindow();
    }

    new Notification({
        title: 'Eye Health Reminder',
        body: 'Focus on something 20 meters away for 20 seconds.'
    }).show();
}

app.whenReady().then(() => {
    createTray();
    triggerPopup();
    setInterval(() => {
        triggerPopup();
    }, DELAY);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
