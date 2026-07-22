# Ghost Overlay

> *This is some questionable project I'm getting into. What are the odds to crack interviews now?*

---

### 19/7/26

Let's see, here's something to look forward to:

```text
ghost/
│
├── main.py
├── overlay.py
├── controller.py
├── win32.py
├── widgets/
│      ├── ghost_frame.py
│      ├── text_panel.py
│      └── resize_handles.py
│
├── utils/
       ├── hotkeys.py
       └── settings.py
```

#### Module Structure

* **`main.py`**
  * entry point
  * creates the QApplication
  * load config
  * instantiate controller
  * show overlay
  * start the QT event loop

* **`overlay.py`**
  * defines the ghost window
  * does not contain business logic

* **`controller.py`**
  * connects everything together
  * react to hotkeys
  * toggle stuff
  * text update
  * events
  * UI API connetion

* **`win32.py`**
  * contains all Windows specific code

* **`widgets/ghost_frame.py`**
  * defines visual container

* **`widgets/text_panel.py`**
  * displays text

* **`widgets/resize_handles.py`**
  * handles resizing

* **`utils/hotkeys.py`**
  * keyboard shortcuts

* **`utils/settings.py`**
  * app configuration

* **`assets/`**
  * static resourcces

---

### 22/7/26

> So far, the actual project has two instances right now. One is backup.py which has eveything together in a single script, but is nor exactly the best solution out there. So I built the rest of the project with a better structure. The entrypoint of the larger project is at main.py as shown in the file map or whatever they call it, I don't remember.