import os, json, time, math, random, threading, platform
import tkinter as tk
from collections import deque
from PIL import Image, ImageTk, ImageDraw, ImageEnhance
import sys
from pathlib import Path


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR   = get_base_dir()
CONFIG_DIR = BASE_DIR / "config"
API_FILE   = CONFIG_DIR / "api_keys.json"

SYSTEM_NAME = "J.A.R.V.I.S"
MODEL_BADGE = "KAIRO"
DEVELOPER   = "SUBHANSH"
STUDIO      = "NEARX STUDIOS"

def _load_user_name():
    try:
        api_file = get_base_dir() / "config" / "api_keys.json"
        data = json.loads(api_file.read_text(encoding="utf-8"))
        return data.get("user_name", "OPERATOR").upper()
    except Exception:
        return "OPERATOR"

YOUR_NAME = _load_user_name()

# ── Magenta / Cyan / Purple / Silver palette ──────────────────────────────────
C_BG       = "#000000"          # near-black deep purple void
C_BG2      = "#000000"          # slightly lighter bg for panels
C_PRI      = "#00f5ff"          # electric cyan
C_MAG      = "#ff00cc"          # hot magenta
C_PURP     = "#9b30ff"          # vivid purple
C_PURP2    = "#5a0099"          # deep purple
C_SILVER   = "#b8c8d8"          # cool silver
C_SILVER2  = "#607080"          # dim silver
C_DIM      = "#1a0030"          # very dim purple
C_TEXT     = "#d0f0ff"          # light cyan text
C_GREEN    = "#00ffaa"          # neon mint
C_RED      = "#ff2255"          # red-pink error
C_YELLOW   = "#ffdd00"          # gold
C_PANEL    = "#050505"          # panel bg
C_GLOW_C   = "#00d4ff"          # cyan glow
C_GLOW_M   = "#cc00aa"          # magenta glow


def hex_points(cx, cy, r, rotation=0):
    pts = []
    for i in range(6):
        a = math.radians(60 * i + rotation)
        pts.append(cx + r * math.cos(a))
        pts.append(cy + r * math.sin(a))
    return pts


def diamond_points(cx, cy, w, h):
    return [cx, cy - h, cx + w, cy, cx, cy + h, cx - w, cy]


CODE_LINES = [
    "neural.matrix.init()",
    "kairo.sync(user='SUBHANSH')",
    "∴ gemini_2_5.stream()",
    "∴ voice.pipeline.start()",
    "mem.recall(depth='infinite')",
    "∵ threat_scan = NONE",
    "clap.detect.armed = True",
    "telegram.bridge.uplink()",
    "∴ tools.manifest.load()",
    "encrypt(mode='AES-512')",
    "inference.amd.cloud.on()",
    "∵ vision.camera.active",
    "∴ screen.capture.ready()",
    "bio.id = VERIFIED",
    "∵ response.latency = 42ms",
    "uptime.tick(interval=1)",
    "∴ persona.kairo.v9.1()",
    "∵ memory.persist.write()",
    "action.queue.flush()",
    "∴ status = NOMINAL",
]

GLITCH_CHARS = "▓░▒█▄▀■□◆◇⬡⬢⟁△▽◈"


class JarvisUI:
    def __init__(self, face_path, size=None):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S — KAIRO v9.1")
        self.root.resizable(False, False)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        W  = min(sw, 1100)
        H  = min(sh, 800)
        self.root.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")
        self.root.configure(bg=C_BG)

        self.W = W
        self.H = H

        # ── Layout: LEFT = orb zone (40%), RIGHT = data zone (60%) ───────────
        self.ORB_ZONE_W = int(W * 0.40)
        self.DATA_ZONE_X = self.ORB_ZONE_W
        self.DATA_ZONE_W = W - self.ORB_ZONE_W

        self.FACE_SZ = min(int(H * 0.38), 290)
        self.FCX     = self.ORB_ZONE_W // 2
        self.FCY     = int(H * 0.42)

        # ── State ─────────────────────────────────────────────────────────────
        self.speaking      = False
        self.muted         = False
        self.scale         = 1.0
        self.target_scale  = 1.0
        self.halo_a        = 60.0
        self.target_halo   = 60.0
        self.last_t        = time.time()
        self.tick          = 0
        self.scan_angle    = 0.0
        self.scan2_angle   = 180.0
        self.scan3_angle   = 90.0
        self.pulse_r       = [0.0, self.FACE_SZ * 0.3, self.FACE_SZ * 0.6]
        self.status_text   = "INITIALISING"
        self.status_blink  = True
        self._jarvis_state = "INITIALISING"
        self.typing_queue  = deque()
        self.is_typing     = False
        self.on_text_command = None
        self._face_pil         = None
        self._has_face         = False
        self._face_scale_cache = None

        self._start_time  = time.time()
        self._mem_used    = random.uniform(2.1, 3.8)
        self._cpu_load    = random.uniform(12, 35)
        self._net_ping    = random.randint(18, 64)
        self._code_offset = 0
        self._glitch_timer = 0
        self._glitch_active = False
        self._glitch_text   = ""

        # ── Ring system ───────────────────────────────────────────────────────
        self._rings = [
            # (r_frac, speed, arc_len, gap, width, color_mode, phase)
            # color_mode: 0=cyan, 1=magenta, 2=purple, 3=silver
            (0.54, 1.2,  110, 55, 3, 0,  0.0),
            (0.48, -0.9, 85,  48, 2, 1, 60.0),
            (0.42, 1.7,  65,  38, 2, 2, 120.0),
            (0.36, -1.4, 50,  32, 1, 0, 180.0),
            (0.30, 2.1,  38,  28, 1, 1, 240.0),
            (0.24, -1.8, 28,  22, 1, 3, 300.0),
        ]
        self._energy_dots = [
            (random.uniform(0, 360), random.uniform(0.26, 0.52),
             random.uniform(1.2, 3.2), random.randint(0, 2))
            for _ in range(32)
        ]
        self._data_arcs = [(i * 60.0, random.uniform(0.4, 0.9), i % 3)
                           for i in range(6)]
        self._inner_spin = [i * 45.0 for i in range(8)]
        self._hex_ring   = [i * 60.0 for i in range(6)]

        # Random glowing background elements
        random.seed(42)
        self._bg_particles = [
            (random.randint(0, 1100), random.randint(0, 800),
             random.uniform(0.5, 2.5), random.randint(0, 3),
             random.uniform(0, math.pi * 2))
            for _ in range(60)
        ]
        self._bg_hexagons = [
            (random.randint(0, 1100), random.randint(0, 800),
             random.randint(12, 55), random.randint(0, 2),
             random.uniform(0, math.pi * 2))
            for _ in range(18)
        ]
        self._bg_lines = [
            (random.randint(0, 1100), random.randint(0, 800),
             random.uniform(0, math.pi * 2), random.randint(20, 120),
             random.randint(0, 3))
            for _ in range(24)
        ]
        self._bg_circles = [
            (random.randint(0, 1100), random.randint(0, 800),
             random.randint(8, 40), random.randint(0, 3))
            for _ in range(20)
        ]
        self._bg_spin = 0.0
        random.seed()  # restore randomness
        self._diamond_spin = 0.0
        self._tri_spin    = [0.0, 120.0, 240.0]

        # Right panel data streams
        self._stream_lines = [""] * 16
        self._stream_offset = 0
        self._metric_bars   = {
            "NEURAL": random.uniform(60, 90),
            "VOICE ": random.uniform(40, 75),
            "VISION": random.uniform(50, 85),
            "MEMORY": random.uniform(30, 60),
            "UPLINK": random.uniform(70, 95),
        }

        self._load_face(face_path)

        self.bg = tk.Canvas(self.root, width=W, height=H,
                            bg=C_BG, highlightthickness=0)
        self.bg.place(x=0, y=0)

        # ── RIGHT PANEL: log + input ──────────────────────────────────────────
        LOG_X = self.DATA_ZONE_X + 20
        LOG_W = self.DATA_ZONE_W - 40
        LOG_Y = int(H * 0.13)
        LOG_H = int(H * 0.48)

        self.log_frame = tk.Frame(self.root, bg=C_PANEL,
                                  highlightbackground=C_PURP2,
                                  highlightthickness=1)
        self.log_frame.place(x=LOG_X, y=LOG_Y, width=LOG_W, height=LOG_H)

        # Log header label
        self._log_header = tk.Canvas(self.log_frame, width=LOG_W - 2,
                                      height=22, bg=C_PANEL, highlightthickness=0)
        self._log_header.pack(side="top", fill="x")
        self._log_header.create_rectangle(0, 0, LOG_W, 22, fill="#000000", outline="")
        self._log_header.create_text(10, 11, text="◈ NEURAL COMM LINK",
                                      fill=C_PURP, font=("Courier", 8, "bold"), anchor="w")
        self._log_header.create_text(LOG_W - 10, 11, text="ENCRYPTED",
                                      fill=C_SILVER2, font=("Courier", 7), anchor="e")

        self.log_text = tk.Text(self.log_frame, fg=C_TEXT, bg=C_PANEL,
                                insertbackground=C_PRI, borderwidth=0,
                                wrap="word", font=("Courier", 9), padx=10, pady=6)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")
        self.log_text.tag_config("you",  foreground=C_SILVER)
        self.log_text.tag_config("ai",   foreground=C_PRI)
        self.log_text.tag_config("sys",  foreground=C_PURP)
        self.log_text.tag_config("err",  foreground=C_RED)

        # ── Metric bars panel ─────────────────────────────────────────────────
        METRICS_Y = LOG_Y + LOG_H + 10
        METRICS_H = 110
        self.metrics_canvas = tk.Canvas(self.root, width=LOG_W, height=METRICS_H,
                                         bg=C_PANEL, highlightbackground=C_PURP2,
                                         highlightthickness=1)
        self.metrics_canvas.place(x=LOG_X, y=METRICS_Y)

        # ── Input bar ─────────────────────────────────────────────────────────
        INPUT_Y = METRICS_Y + METRICS_H + 10
        self._build_input_bar(LOG_W, LOG_X, INPUT_Y)

        # ── Mute button (left panel bottom) ──────────────────────────────────
        self._build_mute_button()

        # ── Bottom status strip ───────────────────────────────────────────────
        self._build_bottom_bar()

        self.root.bind("<F4>", lambda e: self._toggle_mute())

        self._api_key_ready = self._api_keys_exist()
        if not self._api_key_ready:
            self._show_setup_ui()

        self._scroll_code()
        self._update_metrics()
        self._animate()
        self.root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

    # ── Public API ────────────────────────────────────────────────────────────
    def toggle_mute(self):
        self._toggle_mute()

    def set_state(self, state: str):
        self._jarvis_state = state
        lut = {
            "MUTED":      ("MUTED",      False),
            "SPEAKING":   ("SPEAKING",   True),
            "THINKING":   ("THINKING",   False),
            "LISTENING":  ("LISTENING",  False),
            "PROCESSING": ("PROCESSING", False),
        }
        txt, spk = lut.get(state, ("ONLINE", False))
        self.status_text = txt
        self.speaking    = spk

    def write_log(self, text: str):
        self.typing_queue.append(text)
        tl = text.lower()
        if tl.startswith("you:"):
            self.set_state("PROCESSING")
        elif tl.startswith("jarvis:") or tl.startswith("ai:"):
            self.set_state("SPEAKING")
        if not self.is_typing:
            self._start_typing()

    def start_speaking(self): self.set_state("SPEAKING")
    def stop_speaking(self):
        if not self.muted: self.set_state("LISTENING")

    def wait_for_api_key(self):
        while not self._api_key_ready:
            time.sleep(0.1)

    # ── Build helpers ─────────────────────────────────────────────────────────
    def _build_bottom_bar(self):
        BAR_H = 36
        BAR_Y = self.H - BAR_H
        self._bottom = tk.Canvas(self.root, width=self.W, height=BAR_H,
                                  bg="#000000", highlightthickness=0)
        self._bottom.place(x=0, y=BAR_Y)
        self._bottom.create_line(0, 0, self.W, 0, fill=C_PURP2, width=1)

        items = [
            ("◈ KAIRO v9.1", C_PURP),
            ("AMD CLOUD", C_SILVER2),
            ("GEMINI 2.5 FLASH", C_SILVER2),
            ("[F4] MUTE", C_SILVER2),
            (f"USER: {YOUR_NAME}", C_MAG),
            (f"DEV: {DEVELOPER}  ·  {STUDIO}", C_SILVER2),
        ]
        spacing = self.W // (len(items) + 1)
        for i, (label, col) in enumerate(items):
            self._bottom.create_text((i + 1) * spacing, BAR_H // 2,
                                      text=label, fill=col, font=("Courier", 8))

    def _build_mute_button(self):
        self._mute_canvas = tk.Canvas(self.root, width=130, height=34,
                                       bg=C_BG, highlightthickness=0, cursor="hand2")
        self._mute_canvas.place(x=int(self.ORB_ZONE_W * 0.5) - 65,
                                 y=self.H - 80)
        self._mute_canvas.bind("<Button-1>", lambda e: self._toggle_mute())
        self._draw_mute_button()

    def _draw_mute_button(self):
        c = self._mute_canvas
        c.delete("all")
        if self.muted:
            border, fill, label, fg = C_RED, "#1a0010", "⊘  MIC  OFF", C_RED
        else:
            border, fill, label, fg = C_MAG, "#100020", "◉  MIC   ON", C_MAG
        c.create_rectangle(0, 0, 130, 34, outline=border, fill=fill, width=1)
        # corner accents
        for bx, by, dx, dy in [(0,0,8,0),(0,0,0,8),(122,0,130,0),(130,0,130,8),
                                 (0,26,0,34),(0,34,8,34),(122,34,130,34),(130,26,130,34)]:
            c.create_line(bx, by, dx, dy, fill=border, width=1)
        c.create_text(65, 17, text=label, fill=fg, font=("Courier", 10, "bold"))

    def _toggle_mute(self):
        self.muted = not self.muted
        self._draw_mute_button()
        if self.muted:
            self.set_state("MUTED")
            self.write_log("SYS: Microphone muted.")
        else:
            self.set_state("LISTENING")
            self.write_log("SYS: Microphone active.")

    def _build_input_bar(self, lw, x0, y):
        BTN_W = 90
        INP_W = lw - BTN_W - 6
        self._input_var = tk.StringVar()
        self._input_entry = tk.Entry(
            self.root, textvariable=self._input_var,
            fg=C_TEXT, bg="#000000",
            insertbackground=C_MAG,
            borderwidth=0, font=("Courier", 10),
            highlightthickness=1,
            highlightbackground=C_PURP2,
            highlightcolor=C_MAG,
        )
        self._input_entry.place(x=x0, y=y, width=INP_W, height=30)
        self._input_entry.bind("<Return>", self._on_input_submit)

        self._send_btn = tk.Button(
            self.root, text="▶  EXEC",
            command=self._on_input_submit,
            fg=C_BG, bg=C_MAG,
            activeforeground=C_BG, activebackground=C_PRI,
            font=("Courier", 9, "bold"),
            borderwidth=0, cursor="hand2",
        )
        self._send_btn.place(x=x0 + INP_W + 6, y=y, width=BTN_W, height=30)

    def _on_input_submit(self, event=None):
        text = self._input_var.get().strip()
        if not text:
            return
        self._input_var.set("")
        self.write_log(f"You: {text}")
        if self.on_text_command:
            threading.Thread(target=self.on_text_command, args=(text,), daemon=True).start()

    # ── Code scroll ───────────────────────────────────────────────────────────
    def _scroll_code(self):
        self._code_offset = (self._code_offset + 1) % len(CODE_LINES)
        self.root.after(500, self._scroll_code)

    # ── Metric bar updates ────────────────────────────────────────────────────
    def _update_metrics(self):
        for key in self._metric_bars:
            delta = random.uniform(-3, 3)
            if self.speaking:
                delta = random.uniform(-5, 8)
            self._metric_bars[key] = max(5, min(98, self._metric_bars[key] + delta))
        self._cpu_load  = max(5, min(95, self._cpu_load + random.uniform(-2, 2)))
        self._mem_used  = max(1.0, min(8.0, self._mem_used + random.uniform(-0.04, 0.04)))
        self._net_ping  = max(8, min(200, self._net_ping + random.randint(-3, 3)))
        self.root.after(800, self._update_metrics)

    # ── Face loading ──────────────────────────────────────────────────────────
    def _load_face(self, path):
        FW = self.FACE_SZ
        try:
            img  = Image.open(path).convert("RGBA").resize((FW, FW), Image.LANCZOS)
            mask = Image.new("L", (FW, FW), 0)
            ImageDraw.Draw(mask).ellipse((2, 2, FW-2, FW-2), fill=255)
            img.putalpha(mask)
            self._face_pil = img
            self._has_face = True
        except Exception:
            self._has_face = False

    @staticmethod
    def _ac(r, g, b, a):
        f = a / 255.0
        return f"#{int(r*f):02x}{int(g*f):02x}{int(b*f):02x}"

    def _ring_color(self, mode, alpha, bright=1.0):
        a = max(0, min(255, int(alpha * bright)))
        if self.muted:
            return self._ac(255, 30, 80, a)
        if mode == 0: return self._ac(0,   245, 255, a)   # cyan
        if mode == 1: return self._ac(255, 0,   200, a)   # magenta
        if mode == 2: return self._ac(155, 48,  255, a)   # purple
        return          self._ac(184, 200, 216, a)         # silver

    # ── Animation loop ────────────────────────────────────────────────────────
    def _animate(self):
        self.tick += 1
        now = time.time()

        if now - self.last_t > (0.12 if self.speaking else 0.5):
            if self.speaking:
                self.target_scale = random.uniform(1.04, 1.10)
                self.target_halo  = random.uniform(140, 190)
            elif self.muted:
                self.target_scale = random.uniform(0.998, 1.001)
                self.target_halo  = random.uniform(18, 30)
            else:
                self.target_scale = random.uniform(1.001, 1.006)
                self.target_halo  = random.uniform(52, 72)
            self.last_t = now

        sp = 0.35 if self.speaking else 0.16
        self.scale  += (self.target_scale - self.scale) * sp
        self.halo_a += (self.target_halo  - self.halo_a) * sp

        spd = 1.8 if self.speaking else 0.85
        self.scan_angle  = (self.scan_angle  + spd * 1.6) % 360
        self.scan2_angle = (self.scan2_angle - spd * 1.0) % 360
        self.scan3_angle = (self.scan3_angle + spd * 2.2) % 360

        pspd  = 4.0 if self.speaking else 1.9
        limit = self.FACE_SZ * 0.74
        new_p = [r + pspd for r in self.pulse_r if r + pspd < limit]
        if len(new_p) < 3 and random.random() < (0.07 if self.speaking else 0.025):
            new_p.append(0.0)
        self.pulse_r = new_p

        if self.tick % 38 == 0:
            self.status_blink = not self.status_blink

        # rings
        self._rings = [
            (rf, sp2, al, g, w, cm, (ph + sp2 * spd) % 360)
            for rf, sp2, al, g, w, cm, ph in self._rings
        ]
        self._inner_spin = [(a + (2.8 if self.speaking else 1.2)) % 360
                            for a in self._inner_spin]
        self._data_arcs  = [((a + (1.6 if self.speaking else 0.7)) % 360, v, cm)
                            for a, v, cm in self._data_arcs]
        self._energy_dots = [
            ((a + random.uniform(0.2, 0.9)) % 360, r, s, cm)
            for a, r, s, cm in self._energy_dots
        ]
        self._hex_ring = [(a + (0.8 if self.speaking else 0.35)) % 360
                          for a in self._hex_ring]
        self._diamond_spin = (self._diamond_spin + (1.5 if self.speaking else 0.6)) % 360
        self._bg_spin = (self._bg_spin + 0.15) % 360
        self._tri_spin = [(a + (2.2 if self.speaking else 0.9)) % 360
                          for a in self._tri_spin]

        # glitch effect
        self._glitch_timer += 1
        if self._glitch_timer > random.randint(120, 300):
            self._glitch_active = True
            self._glitch_text   = "".join(random.choice(GLITCH_CHARS) for _ in range(8))
            self._glitch_timer  = 0
        elif self._glitch_active and self._glitch_timer > 6:
            self._glitch_active = False

        self._draw()
        self.root.after(16, self._animate)

    # ── Main draw ─────────────────────────────────────────────────────────────
    def _draw(self):
        c    = self.bg
        W, H = self.W, self.H
        t    = self.tick
        FCX  = self.FCX
        FCY  = self.FCY
        FW   = self.FACE_SZ
        OZW  = self.ORB_ZONE_W
        DZX  = self.DATA_ZONE_X
        c.delete("all")

        # ── Background ────────────────────────────────────────────────────────
        c.create_rectangle(0, 0, W, H, fill=C_BG, outline="")

        # ── Random glowing background designs ────────────────────────────────────
        glow_colors = [
            lambda a: self._ac(255, 0, 200, a),   # magenta
            lambda a: self._ac(0, 245, 255, a),    # cyan
            lambda a: self._ac(155, 48, 255, a),   # purple
            lambda a: self._ac(184, 200, 216, a),  # silver
        ]
        bg_spin_r = math.radians(self._bg_spin)

        # Glowing floating particles (pulsing)
        for i, (px, py, sz, cm, phase) in enumerate(self._bg_particles):
            pulse = abs(math.sin(t * 0.03 + phase + i * 0.4))
            a = max(0, min(255, int(18 + 55 * pulse)))
            col = glow_colors[cm](a)
            c.create_oval(px-sz, py-sz, px+sz, py+sz, fill=col, outline='')
            # soft outer glow ring
            a2 = max(0, int(a * 0.3))
            col2 = glow_colors[cm](a2)
            sr2 = sz * 2.2
            c.create_oval(px-sr2, py-sr2, px+sr2, py+sr2, fill='', outline=col2, width=1)

        # Glowing hexagons scattered around
        for i, (hx2, hy2, hr3, cm, phase) in enumerate(self._bg_hexagons):
            rot = math.degrees(bg_spin_r * (0.3 + i * 0.07) + phase)
            pts = hex_points(hx2, hy2, hr3, rotation=rot)
            pulse = abs(math.sin(t * 0.02 + phase + i * 0.6))
            a = max(0, min(255, int(8 + 35 * pulse)))
            col = glow_colors[cm](a)
            c.create_polygon(pts, outline=col, fill='', width=1)
            # inner smaller hex
            pts2 = hex_points(hx2, hy2, int(hr3 * 0.55), rotation=rot + 30)
            a2 = max(0, int(a * 0.5))
            col2 = glow_colors[(cm+1)%4](a2)
            c.create_polygon(pts2, outline=col2, fill='', width=1)

        # Glowing line segments
        for i, (lx, ly, angle, length, cm) in enumerate(self._bg_lines):
            pulse = abs(math.sin(t * 0.025 + i * 0.5))
            a = max(0, min(255, int(10 + 45 * pulse)))
            col = glow_colors[cm](a)
            ex = lx + length * math.cos(angle + bg_spin_r * 0.1)
            ey = ly + length * math.sin(angle + bg_spin_r * 0.1)
            c.create_line(lx, ly, ex, ey, fill=col, width=1)
            # glow duplicate
            a2 = max(0, int(a * 0.25))
            col2 = glow_colors[cm](a2)
            c.create_line(lx-1, ly-1, ex-1, ey-1, fill=col2, width=2)

        # Glowing arc circles
        for i, (cx2, cy2, cr, cm) in enumerate(self._bg_circles):
            pulse = abs(math.sin(t * 0.028 + i * 0.7))
            a = max(0, min(255, int(8 + 30 * pulse)))
            col = glow_colors[cm](a)
            start_a = (self._bg_spin * 2 + i * 37) % 360
            c.create_arc(cx2-cr, cy2-cr, cx2+cr, cy2+cr,
                         start=start_a, extent=200, outline=col, width=1, style='arc')
            c.create_arc(cx2-cr*1.6, cy2-cr*1.6, cx2+cr*1.6, cy2+cr*1.6,
                         start=start_a+120, extent=100, outline=glow_colors[(cm+2)%4](max(0,int(a*0.4))), width=1, style='arc')

        # Fine grid — left orb zone
        for x in range(0, OZW, 32):
            c.create_line(x, 0, x, H, fill="#080008", width=1)
        for y in range(0, H, 32):
            c.create_line(0, y, OZW, y, fill="#080008", width=1)

        # Coarser grid — right data zone
        for x in range(DZX, W, 48):
            c.create_line(x, 0, x, H, fill="#000000", width=1)
        for y in range(0, H, 48):
            c.create_line(DZX, y, W, y, fill="#000000", width=1)

        # Divider line
        c.create_line(OZW, 0, OZW, H, fill=C_PURP2, width=1)
        c.create_line(OZW+1, 0, OZW+1, H, fill=self._ac(155, 48, 255, 40), width=1)
        # Divider glow pulse
        glow_div = int(60 + 40 * math.sin(t * 0.04))
        for i in range(3):
            gc = self._ac(155, 48, 255, max(0, glow_div - i*18))
            c.create_line(OZW - i, 0, OZW - i, H, fill=gc, width=1)

        # ── Header bar ────────────────────────────────────────────────────────
        HDR = 60
        c.create_rectangle(0, 0, W, HDR, fill="#000000", outline="")
        c.create_line(0, HDR, W, HDR, fill=C_PURP2, width=1)

        # Header glow line
        glow_h = int(160 + 80 * math.sin(t * 0.04))
        for i, (col, w2) in enumerate([(self._ac(255,0,200,int(glow_h*0.3)),3),
                                        (self._ac(255,0,200,int(glow_h*0.6)),2),
                                        (self._ac(255,0,200,glow_h),1)]):
            c.create_line(0, i, W, i, fill=col, width=1)

        # Dashed moving line
        dash_off = (t * 3) % 80
        for dx in range(int(dash_off), W, 80):
            c.create_line(dx, 2, dx+40, 2, fill=self._ac(0,245,255,50), width=1)

        # Title
        title_col = C_RED if self.muted else C_PRI
        c.create_text(OZW // 2, 20, text=SYSTEM_NAME,
                      fill=title_col, font=("Courier", 22, "bold"))
        if self._glitch_active:
            c.create_text(OZW // 2 + random.randint(-3, 3), 20,
                          text=self._glitch_text[:6],
                          fill=self._ac(255,0,200,120), font=("Courier", 22, "bold"))

        c.create_text(OZW // 2, 44,
                      text="I'm not AI-powered, I'm AI-possessed. There's a difference",
                      fill=C_PURP, font=("Courier", 7))

        # Right header info
        c.create_text(DZX + 16, 18, text=f"◈ {MODEL_BADGE}",
                      fill=C_MAG, font=("Courier", 12, "bold"), anchor="w")
        c.create_text(DZX + 16, 38, text="NEURAL INFERENCE ENGINE",
                      fill=C_SILVER2, font=("Courier", 8), anchor="w")
        c.create_text(W - 16, 18, text=time.strftime("%H:%M:%S"),
                      fill=C_PRI, font=("Courier", 18, "bold"), anchor="e")
        c.create_text(W - 16, 42, text=time.strftime("%d · %b · %Y"),
                      fill=C_SILVER2, font=("Courier", 8), anchor="e")

        # ── Right data zone: system info strip ────────────────────────────────
        INFO_Y = HDR + 8
        info_items = [
            ("CPU", f"{self._cpu_load:.1f}%"),
            ("MEM", f"{self._mem_used:.1f}GB"),
            ("PING", f"{self._net_ping}ms"),
            ("USER", YOUR_NAME),
            ("OS", "WINDOWS"),
            ("VER", "9.1.0"),
        ]
        ix = DZX + 20
        for label, val in info_items:
            c.create_text(ix, INFO_Y + 4, text=label, fill=C_SILVER2,
                          font=("Courier", 7), anchor="w")
            c.create_text(ix, INFO_Y + 16, text=val, fill=C_SILVER,
                          font=("Courier", 8, "bold"), anchor="w")
            ix += (self.DATA_ZONE_W - 40) // len(info_items)

        # ── Right zone: metric bars (drawn directly on main canvas) ──────────
        MBX  = DZX + 20
        MBY  = self.H - 200
        MBW  = self.DATA_ZONE_W - 40
        bar_w_each = MBW // len(self._metric_bars)
        for i, (label, val) in enumerate(self._metric_bars.items()):
            bx    = MBX + i * bar_w_each
            filled = int((bar_w_each - 10) * val / 100)
            col   = (C_RED if val > 90 else C_YELLOW if val > 70 else
                     [C_PRI, C_MAG, C_PURP, C_GREEN, C_SILVER][i % 5])
            c.create_rectangle(bx, MBY, bx + bar_w_each - 10, MBY + 6,
                                outline=C_DIM, fill="#0c0020")
            c.create_rectangle(bx, MBY, bx + filled, MBY + 6,
                                fill=col, outline="")
            c.create_text(bx + (bar_w_each - 10) // 2, MBY + 16,
                          text=label.strip(), fill=C_SILVER2, font=("Courier", 7))
            c.create_text(bx + (bar_w_each - 10) // 2, MBY + 26,
                          text=f"{val:.0f}%", fill=col, font=("Courier", 7, "bold"))

        # ── Scrolling code waterfall in right background ──────────────────────
        code_cols = [DZX + 20, DZX + self.DATA_ZONE_W // 2]
        for col_x in code_cols:
            for row in range(14):
                idx = (self._code_offset + row + int(col_x)) % len(CODE_LINES)
                cy2 = HDR + 36 + row * 28
                alpha_val = max(20, 60 - row * 4)
                tc = self._ac(100, 0, 180, alpha_val)
                c.create_text(col_x, cy2, text=CODE_LINES[idx][:28],
                              fill=tc, font=("Courier", 7), anchor="w")

        # ── ORB ZONE ──────────────────────────────────────────────────────────
        # Outer hex frame
        for hr, lw2 in [(FW * 0.72, 1), (FW * 0.68, 1)]:
            pts = hex_points(FCX, FCY, int(hr), rotation=self._hex_ring[0] * 0.05)
            c.create_polygon(pts, outline=C_DIM, fill="", width=lw2)

        # Atmosphere glow
        atm_r = int(FW * 0.70)
        for i in range(20, 0, -1):
            r2   = int(atm_r * i / 20)
            frac = (i / 20) ** 2
            ga   = max(0, min(255, int(self.halo_a * 0.07 * frac)))
            if self.muted:
                col = self._ac(255, 30, 80,  ga)
            else:
                # alternating cyan/magenta/purple atmosphere
                if i % 3 == 0:   col = self._ac(0,   200, 255, ga)
                elif i % 3 == 1: col = self._ac(200, 0,   180, ga)
                else:             col = self._ac(120, 40,  255, ga)
            c.create_oval(FCX-r2, FCY-r2, FCX+r2, FCY+r2, fill=col, outline="")

        # 6 spinning rings
        for r_frac, spd2, arc_l, gap, w_ring, cm, phase in self._rings:
            ring_r = int(FW * r_frac)
            a_base = max(0, min(255, int(self.halo_a * 1.1)))
            step   = arc_l + gap
            for s in range(360 // max(1, step) + 1):
                start = (phase + s * step) % 360
                col   = self._ring_color(cm, a_base)
                c.create_arc(FCX - ring_r, FCY - ring_r,
                             FCX + ring_r, FCY + ring_r,
                             start=start, extent=arc_l,
                             outline=col, width=w_ring, style="arc")
            # dim gaps
            for s in range(360 // max(1, step) + 1):
                start = (phase + s * step + arc_l) % 360
                col   = self._ring_color(cm, int(a_base * 0.08))
                c.create_arc(FCX - ring_r, FCY - ring_r,
                             FCX + ring_r, FCY + ring_r,
                             start=start, extent=gap,
                             outline=col, width=1, style="arc")

        # 32 energy dots
        for angle, r_frac, dot_sz, cm in self._energy_dots:
            ring_r = int(FW * r_frac)
            rad    = math.radians(angle)
            dx2    = FCX + ring_r * math.cos(rad)
            dy2    = FCY - ring_r * math.sin(rad)
            a_val  = max(0, min(255, int(self.halo_a * 2.0)))
            col    = self._ring_color(cm, a_val, 1.2)
            sr     = dot_sz
            c.create_oval(dx2-sr, dy2-sr, dx2+sr, dy2+sr, fill=col, outline="")

        # 6 data arc segments
        data_r = int(FW * 0.57)
        for angle, intensity, cm in self._data_arcs:
            a_val = max(0, min(255, int(self.halo_a * 1.6 * intensity)))
            col   = self._ring_color(cm, a_val)
            c.create_arc(FCX-data_r, FCY-data_r, FCX+data_r, FCY+data_r,
                         start=angle, extent=20, outline=col, width=5, style="arc")
            trail_c = self._ring_color(cm, int(a_val * 0.3))
            c.create_arc(FCX-data_r, FCY-data_r, FCX+data_r, FCY+data_r,
                         start=angle-22, extent=22, outline=trail_c, width=2, style="arc")

        # Triple scanner
        for sr_frac, sang, ext, w_s, am, cm in [
                (0.55, self.scan_angle,         1.0, 3, 1.4, 0),
                (0.51, self.scan2_angle,         0.7, 2, 0.9, 1),
                (0.59, self.scan3_angle,         0.5, 1, 0.5, 2)]:
            sr    = int(FW * sr_frac)
            arc_e = int((72 if self.speaking else 44) * ext)
            a_val = min(255, int(self.halo_a * am))
            col   = self._ring_color(cm, a_val)
            c.create_arc(FCX-sr, FCY-sr, FCX+sr, FCY+sr,
                         start=sang, extent=arc_e, outline=col, width=w_s, style="arc")

        # Tick marks
        t_out = int(FW * 0.545)
        t_in  = int(FW * 0.520)
        for deg in range(0, 360, 5):
            rad = math.radians(deg)
            inn = t_in if deg % 30 == 0 else (t_in + 3 if deg % 15 == 0 else t_in + 6)
            ww  = 2 if deg % 30 == 0 else 1
            if deg % 30 == 0:
                col = self._ac(0, 245, 255, 160) if not self.muted else self._ac(255,30,80,160)
            elif deg % 15 == 0:
                col = self._ac(155, 48, 255, 120) if not self.muted else self._ac(255,30,80,80)
            else:
                col = self._ac(80, 0, 140, 70) if not self.muted else self._ac(180,0,60,50)
            c.create_line(FCX + t_out * math.cos(rad), FCY - t_out * math.sin(rad),
                          FCX + inn  * math.cos(rad), FCY - inn  * math.sin(rad),
                          fill=col, width=ww)

        # Rotating diamond frame
        diam_r = int(FW * 0.57)
        da     = math.radians(self._diamond_spin)
        for offset in [0, 90, 180, 270]:
            ang = da + math.radians(offset)
            dx2 = FCX + diam_r * math.cos(ang)
            dy2 = FCY - diam_r * math.sin(ang)
            dm_a = max(0, min(255, int(self.halo_a * 0.7)))
            col  = self._ac(255, 0, 200, dm_a) if not self.muted else self._ac(255,30,80,dm_a)
            c.create_rectangle(dx2-3, dy2-3, dx2+3, dy2+3, fill=col, outline="")

        # Rotating triangles
        for i, t_ang in enumerate(self._tri_spin):
            tri_r = int(FW * [0.53, 0.49, 0.45][i])
            pts   = []
            for v in range(3):
                a2 = math.radians(t_ang + v * 120)
                pts.extend([FCX + tri_r * math.cos(a2), FCY - tri_r * math.sin(a2)])
            t_a = max(0, min(255, int(self.halo_a * 0.18)))
            col = self._ring_color(i, t_a)
            c.create_polygon(pts, outline=col, fill="", width=1)

        # Crosshair
        ch_r = int(FW * 0.56)
        gap  = int(FW * 0.13)
        ch_a = self._ac(0, 245, 255, int(self.halo_a * 0.55)) if not self.muted \
               else self._ac(255, 30, 80, int(self.halo_a * 0.55))
        for x1, y1, x2, y2 in [
                (FCX-ch_r, FCY, FCX-gap, FCY),
                (FCX+gap,  FCY, FCX+ch_r, FCY),
                (FCX, FCY-ch_r, FCX, FCY-gap),
                (FCX, FCY+gap,  FCX, FCY+ch_r)]:
            c.create_line(x1, y1, x2, y2, fill=ch_a, width=1)

        # Crosshair diamonds at ends
        for nx, ny in [(FCX-ch_r,FCY),(FCX+ch_r,FCY),(FCX,FCY-ch_r),(FCX,FCY+ch_r)]:
            pts = diamond_points(nx, ny, 4, 4)
            c.create_polygon(pts, fill=ch_a, outline="")

        # Corner brackets (hex style)
        blen = 24
        bc   = self._ac(0, 245, 255, 220) if not self.muted else self._ac(255, 30, 80, 220)
        bc2  = self._ac(255, 0, 200, 180) if not self.muted else self._ac(255,100,150,180)
        hl = FCX - FW//2; hr2 = FCX + FW//2
        ht = FCY - FW//2; hb  = FCY + FW//2
        for bx, by, sdx, sdy in [(hl, ht, 1,1),(hr2,ht,-1,1),(hl,hb,1,-1),(hr2,hb,-1,-1)]:
            c.create_line(bx, by, bx+sdx*blen, by, fill=bc, width=2)
            c.create_line(bx, by, bx, by+sdy*blen, fill=bc, width=2)
            pts = diamond_points(bx, by, 4, 4)
            c.create_polygon(pts, fill=bc2, outline="")

        # Hex nodes around orbit
        for i, ang_h in enumerate(self._hex_ring):
            hr3  = int(FW * 0.59)
            rad  = math.radians(ang_h)
            hx2  = FCX + hr3 * math.cos(rad)
            hy2  = FCY - hr3 * math.sin(rad)
            ha   = max(0, min(255, int(self.halo_a * 0.8)))
            hcol = self._ring_color(i % 3, ha)
            pts  = hex_points(hx2, hy2, 5, rotation=ang_h)
            c.create_polygon(pts, outline=hcol, fill="", width=1)

        # ── ORB core ──────────────────────────────────────────────────────────
        orb_r = int(FW * 0.24 * self.scale)

        # Outer diffuse glow
        for i in range(22, 0, -1):
            r2   = int(orb_r * 2.4 * i / 22)
            frac = (i / 22) ** 1.8
            ga   = max(0, min(255, int(self.halo_a * 0.06 * frac * frac)))
            if self.muted:
                col = self._ac(255, 30, 80, ga)
            elif i % 3 == 0:
                col = self._ac(0, int(50*frac), int(180*frac), ga)
            elif i % 3 == 1:
                col = self._ac(int(150*frac), 0, int(150*frac), ga)
            else:
                col = self._ac(80, 0, int(200*frac), ga)
            c.create_oval(FCX-r2, FCY-r2, FCX+r2, FCY+r2, fill=col, outline="")

        # Inner solid orb
        for i in range(18, 0, -1):
            r2   = int(orb_r * i / 18)
            frac = i / 18
            ga   = max(0, min(255, int(self.halo_a * 1.7 * frac)))
            if self.muted:
                col = self._ac(int(200*frac), 20, 60, ga)
            elif i > 12:
                col = self._ac(0, int(30*frac), int(180*frac), ga)
            elif i > 6:
                col = self._ac(int(80*frac), 0, int(200*frac), ga)
            else:
                col = self._ac(int(60*frac), int(60*frac), int(255*frac), ga)
            c.create_oval(FCX-r2, FCY-r2, FCX+r2, FCY+r2, fill=col, outline="")

        # Inner spokes
        for i, ang_base in enumerate(self._inner_spin):
            ang = math.radians(ang_base)
            ir  = int(FW * 0.22)
            a_v = max(0, min(255, int(self.halo_a * 0.5)))
            col = self._ring_color(i % 3, a_v)
            c.create_line(FCX, FCY, FCX+ir*math.cos(ang), FCY-ir*math.sin(ang),
                          fill=col, width=1)

        # Core rings
        for rf, ra, rw, cm in [(0.19,0.4,2,0),(0.14,0.25,1,1),(0.09,0.15,1,2)]:
            ir  = int(FW * rf)
            ia  = max(0, min(255, int(self.halo_a * ra)))
            col = self._ring_color(cm, ia)
            c.create_oval(FCX-ir, FCY-ir, FCX+ir, FCY+ir, outline=col, width=rw)

        # Core center
        core_r = int(orb_r * 0.28)
        if self.muted:
            core_c = self._ac(255, 80, 120, 240)
            core_g = self._ac(200, 20, 60,  160)
        else:
            core_c = self._ac(180, 240, 255, 240)
            core_g = self._ac(120, 60,  255, 160)
        c.create_oval(FCX-core_r-5, FCY-core_r-5, FCX+core_r+5, FCY+core_r+5,
                      fill=core_g, outline="")
        c.create_oval(FCX-core_r, FCY-core_r, FCX+core_r, FCY+core_r,
                      fill=core_c, outline="")

        # Specular
        hl_r = max(3, int(core_r * 0.42))
        hl_x = FCX - int(core_r * 0.3)
        hl_y = FCY - int(core_r * 0.3)
        c.create_oval(hl_x-hl_r, hl_y-hl_r, hl_x+hl_r, hl_y+hl_r,
                      fill=self._ac(255,255,255,190), outline="")

        # Pulse rings
        for pr in self.pulse_r:
            pa  = max(0, int(240 * (1.0 - pr / (FW * 0.74))))
            r   = int(pr)
            idx = int(pr * 3 / (FW * 0.74)) % 3
            col = self._ring_color(idx, pa)
            c.create_oval(FCX-r, FCY-r, FCX+r, FCY+r, outline=col, width=2)

        # Face image
        if self._has_face:
            fw = int(FW * self.scale)
            if (self._face_scale_cache is None or
                    abs(self._face_scale_cache[0] - self.scale) > 0.004):
                scaled = self._face_pil.resize((fw, fw), Image.BILINEAR)
                if self.muted:
                    r2, g2, b2, a2 = scaled.split()
                    g2 = ImageEnhance.Brightness(g2).enhance(0.2)
                    b2 = ImageEnhance.Brightness(b2).enhance(0.3)
                    scaled = Image.merge("RGBA", (r2, g2, b2, a2))
                self._face_scale_cache = (self.scale, ImageTk.PhotoImage(scaled))
            c.create_image(FCX, FCY, image=self._face_scale_cache[1])
        else:
            txt_col = self._ac(255,80,120,255) if self.muted else self._ac(180,240,255,255)
            c.create_text(FCX, FCY, text=SYSTEM_NAME,
                          fill=txt_col, font=("Courier", 13, "bold"))

        # ── Status row (below orb) ─────────────────────────────────────────────
        sy = FCY + FW // 2 + 22

        if self.muted:
            stat, sc = "⊘  SYSTEM MUTED", C_RED
        elif self.speaking:
            stat, sc = "◉  SPEAKING", C_MAG
        elif self._jarvis_state == "THINKING":
            sym  = "▶▶▶" if self.status_blink else "———"
            stat, sc = f"{sym}  THINKING", C_YELLOW
        elif self._jarvis_state == "PROCESSING":
            sym  = "▶▶▶" if self.status_blink else "———"
            stat, sc = f"{sym}  PROCESSING", C_PURP
        elif self._jarvis_state == "LISTENING":
            sym  = "◉" if self.status_blink else "○"
            stat, sc = f"{sym}  LISTENING", C_GREEN
        else:
            sym  = "◈" if self.status_blink else "◇"
            stat, sc = f"{sym}  {self.status_text}", C_PRI

        # Status box
        sw2 = 180
        c.create_rectangle(FCX-sw2//2-4, sy-10, FCX+sw2//2+4, sy+12,
                            fill="#000000", outline=C_PURP2)
        c.create_text(FCX, sy, text=stat, fill=sc, font=("Courier", 10, "bold"))

        # Waveform
        wy = sy + 26
        N  = 44
        BH = 20
        bw = int(OZW * 0.85 / N)
        wx0 = (OZW - N * bw) // 2
        for i in range(N):
            if self.muted:
                hb  = int(2 + 1 * math.sin(t * 0.04 + i * 0.25))
                col = C_RED
            elif self.speaking:
                hb  = random.randint(3, BH)
                col = [C_PRI, C_MAG, C_PURP][i % 3]
            else:
                hb  = int(2 + 2 * math.sin(t * 0.07 + i * 0.5))
                col = C_PURP2
            bx = wx0 + i * bw
            c.create_rectangle(bx, wy+BH-hb, bx+bw-1, wy+BH,
                                fill=col, outline="")

        # ── Left sidebar stats strip ──────────────────────────────────────────
        uptime = int(time.time() - self._start_time)
        stats_l = [
            ("UPTIME", f"{uptime//3600:02d}:{(uptime%3600)//60:02d}:{uptime%60:02d}"),
            ("STATUS", self._jarvis_state[:10]),
            ("NET",    "ONLINE"),
            ("ENC",    "AES-512"),
            ("TOOLS",  "15 ACTIVE"),
            ("TG",     "BRIDGED"),
        ]
        sy3 = HDR + 10
        for label, val in stats_l:
            c.create_text(8,       sy3+4, text=label, fill=C_SILVER2,
                          font=("Courier", 7), anchor="w")
            c.create_text(OZW-8,   sy3+4, text=val,   fill=C_SILVER,
                          font=("Courier", 7, "bold"), anchor="e")
            c.create_line(8, sy3+12, OZW-8, sy3+12, fill=C_DIM, width=1)
            sy3 += 18

    # ── Typing log ────────────────────────────────────────────────────────────
    def _start_typing(self):
        if not self.typing_queue:
            self.is_typing = False
            if not self.speaking and not self.muted:
                self.set_state("LISTENING")
            return
        self.is_typing = True
        text = self.typing_queue.popleft()
        tl   = text.lower()
        if tl.startswith("you:"):       tag = "you"
        elif tl.startswith("jarvis:") or tl.startswith("ai:"): tag = "ai"
        elif tl.startswith("err:") or "error" in tl:           tag = "err"
        else:                                                    tag = "sys"
        self.log_text.configure(state="normal")
        self._type_char(text, 0, tag)

    def _type_char(self, text, i, tag):
        if i < len(text):
            self.log_text.insert(tk.END, text[i], tag)
            self.log_text.see(tk.END)
            self.root.after(7, self._type_char, text, i+1, tag)
        else:
            self.log_text.insert(tk.END, "\n")
            self.log_text.configure(state="disabled")
            self.root.after(20, self._start_typing)

    # ── API key check & setup ─────────────────────────────────────────────────
    def _api_keys_exist(self) -> bool:
        if not API_FILE.exists(): return False
        try:
            data = json.loads(API_FILE.read_text(encoding="utf-8"))
            return bool(data.get("gemini_api_key")) and bool(data.get("os_system"))
        except Exception:
            return False

    @staticmethod
    def _detect_os() -> str:
        s = platform.system().lower()
        if s == "darwin":  return "mac"
        if s == "windows": return "windows"
        return "linux"

    def _show_setup_ui(self):
        detected = self._detect_os()
        self._selected_os = tk.StringVar(value=detected)
        self.setup_frame = tk.Frame(self.root, bg="#000000",
                                     highlightbackground=C_MAG, highlightthickness=1)
        self.setup_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.setup_frame, text="◈  KAIRO FIRST BOOT",
                 fg=C_MAG, bg="#000000", font=("Courier", 14, "bold")).pack(pady=(20, 4))
        tk.Label(self.setup_frame, text="Configure neural core before activation.",
                 fg=C_SILVER2, bg="#000000", font=("Courier", 9)).pack(pady=(0, 16))
        tk.Frame(self.setup_frame, bg=C_PURP2, height=1).pack(fill="x", padx=20, pady=(0,12))

        tk.Label(self.setup_frame, text="GEMINI API KEY",
                 fg=C_SILVER2, bg="#000000", font=("Courier", 9)).pack(pady=(0, 4))
        self.gemini_entry = tk.Entry(self.setup_frame, width=54,
                                      fg=C_TEXT, bg="#000000",
                                      insertbackground=C_MAG,
                                      borderwidth=0, font=("Courier", 10), show="*",
                                      highlightthickness=1,
                                      highlightbackground=C_PURP2,
                                      highlightcolor=C_MAG)
        self.gemini_entry.pack(pady=(0, 14))

        tk.Label(self.setup_frame, text="YOUR NAME",
                 fg=C_SILVER2, bg="#000000", font=("Courier", 9)).pack(pady=(0, 4))
        self.name_entry = tk.Entry(self.setup_frame, width=54,
                                    fg=C_TEXT, bg="#000000",
                                    insertbackground=C_MAG,
                                    borderwidth=0, font=("Courier", 10),
                                    highlightthickness=1,
                                    highlightbackground=C_PURP2,
                                    highlightcolor=C_MAG)
        self.name_entry.insert(0, "OPERATOR")
        self.name_entry.pack(pady=(0, 18))

        tk.Frame(self.setup_frame, bg=C_PURP2, height=1).pack(fill="x", padx=20, pady=(0, 12))
        tk.Label(self.setup_frame, text="OPERATING SYSTEM",
                 fg=C_SILVER2, bg="#000000", font=("Courier", 9)).pack(pady=(0, 6))

        detect_label = {"windows": "Windows", "mac": "macOS", "linux": "Linux"}.get(detected, detected)
        tk.Label(self.setup_frame, text=f"AUTO-DETECTED:  {detect_label}",
                 fg=C_YELLOW, bg="#000000", font=("Courier", 8)).pack(pady=(0, 8))

        os_btn_frame = tk.Frame(self.setup_frame, bg="#000000")
        os_btn_frame.pack(pady=(0, 18))
        self._os_buttons = {}
        for os_key, os_label in [("windows","WINDOWS"),("mac","macOS"),("linux","LINUX")]:
            btn = tk.Button(os_btn_frame, text=os_label, width=13,
                            font=("Courier", 10, "bold"), borderwidth=0,
                            cursor="hand2", pady=7,
                            command=lambda k=os_key: self._select_os(k))
            btn.pack(side="left", padx=6)
            self._os_buttons[os_key] = btn
        self._select_os(detected)

        tk.Frame(self.setup_frame, bg=C_PURP2, height=1).pack(fill="x", padx=20, pady=(0,14))
        tk.Button(self.setup_frame, text="◈  ACTIVATE KAIRO",
                  command=self._save_api_keys,
                  bg=C_MAG, fg=C_BG, activebackground=C_PRI, activeforeground=C_BG,
                  font=("Courier", 11, "bold"), borderwidth=0, pady=10,
                  cursor="hand2").pack(pady=(0, 20), padx=30, fill="x")

    def _select_os(self, os_key: str):
        self._selected_os.set(os_key)
        for key, btn in self._os_buttons.items():
            if key == os_key:
                btn.configure(fg=C_BG, bg=C_MAG, activeforeground=C_BG, activebackground=C_MAG)
            else:
                btn.configure(fg=C_SILVER2, bg="#000000",
                              activeforeground=C_TEXT, activebackground=C_DIM)

    def _save_api_keys(self):
        gemini = self.gemini_entry.get().strip()
        if not gemini:
            self.gemini_entry.configure(highlightbackground=C_RED, highlightcolor=C_RED)
            return
        os_system = self._selected_os.get()
        user_name = getattr(self, 'name_entry', None)
        user_name = user_name.get().strip().upper() if user_name else "OPERATOR"
        if not user_name: user_name = "OPERATOR"
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(API_FILE, "w", encoding="utf-8") as f:
            json.dump({"gemini_api_key": gemini, "os_system": os_system,
                       "camera_index": 0, "user_name": user_name}, f, indent=4)
        global YOUR_NAME
        YOUR_NAME = user_name
        self.setup_frame.destroy()
        self._api_key_ready = True
        self.set_state("LISTENING")
        self.write_log(f"SYS: KAIRO online. OS → {os_system.upper()}. Welcome, {user_name}.")