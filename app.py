import os
import tempfile
import urllib.request
import json
import re
from flask import Flask, render_template_string, request, send_file, after_this_request

app = Flask(__name__)

# Interfaz visual de ULTRA TECNOLOGÍA - VERSIÓN RICO V2
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RICO | TIKTOK HD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        
        body {
            background: #000;
            background-image: 
                radial-gradient(at 50% 50%, #1a365d 0%, transparent 50%),
                radial-gradient(at 0% 0%, #d4af37 0%, transparent 20%);
            font-family: 'Orbitron', sans-serif;
            overflow: hidden;
            height: 100vh;
            color: white;
        }

        .money-rain {
            position: absolute;
            top: -60px;
            font-size: 2rem;
            animation: fall linear infinite;
            z-index: 0;
            pointer-events: none;
        }

        @keyframes fall {
            to { transform: translateY(110vh) rotate(360deg); }
        }

        .main-card {
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(25px);
            border: 2px solid #d4af37;
            box-shadow: 0 0 60px rgba(212, 175, 55, 0.3);
            border-radius: 40px;
            padding: 3rem;
            width: 100%;
            max-width: 550px;
            position: relative;
            z-index: 10;
        }

        .gold-text {
            background: linear-gradient(to bottom, #f9f295, #d4af37, #b8860b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
        }

        .input-tech {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(212, 175, 55, 0.4);
            color: #fff;
            padding: 1.25rem;
            border-radius: 15px;
            width: 100%;
            text-align: center;
            font-weight: bold;
            transition: all 0.3s;
        }

        .input-tech:focus {
            border-color: #f9f295;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
            outline: none;
        }

        .btn-hd-rich {
            background: linear-gradient(90deg, #d4af37, #f9f295, #d4af37);
            background-size: 200% auto;
            color: #000;
            font-weight: 900;
            padding: 1.5rem;
            border-radius: 20px;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: -0.5px;
            font-size: 14px;
            cursor: pointer;
            transition: 0.4s;
            animation: shine 2s infinite linear;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        @keyframes shine {
            to { background-position: 200% center; }
        }

        .btn-hd-rich:hover {
            transform: scale(1.03) translateY(-3px);
            box-shadow: 0 15px 30px rgba(212, 175, 55, 0.4);
        }

        .scanner-line {
            width: 100%;
            height: 2px;
            background: #d4af37;
            position: absolute;
            top: 0;
            left: 0;
            animation: scan 3s infinite ease-in-out;
            opacity: 0.3;
            box-shadow: 0 0 15px #d4af37;
        }

        @keyframes scan {
            0%, 100% { top: 0%; }
            50% { top: 100%; }
        }
    </style>
</head>
<body class="flex items-center justify-center">
    <div id="money-bg"></div>

    <div class="main-card overflow-hidden">
        <div class="scanner-line"></div>
        
        <div class="text-center mb-10">
            <h1 class="text-7xl mb-2 gold-text italic">RICO</h1>
            <div class="flex justify-center gap-2 text-2xl mb-4">
                <span>💰</span><span>💎</span><span>💵</span><span>💎</span><span>💰</span>
            </div>
            <p class="text-blue-400 text-[10px] tracking-[0.5em] font-bold uppercase">TikTok High-Tech Extractor</p>
        </div>

        <form action="/download" method="POST" onsubmit="startProcessing()">
            <div class="mb-8">
                <input type="url" name="url" placeholder="PEGA EL LINK AQUÍ" required class="input-tech">
            </div>

            <button id="main-btn" type="submit" class="btn-hd-rich">
                DESCARGAR VIDEO SIN MARCA DE AGUA EN HD
            </button>
        </form>

        <div id="loader" class="hidden mt-8 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-yellow-500 mb-4"></div>
            <p class="text-yellow-400 text-xs font-bold animate-pulse">PROCESANDO RIQUEZA DIGITAL...</p>
        </div>

        <div class="mt-10 pt-6 border-t border-yellow-900/30 text-center">
            <p class="text-[8px] text-yellow-800 tracking-[0.4em] uppercase">Security Level: Gold | Encryption: Active</p>
        </div>
    </div>

    <script>
        // Lluvia de dinero
        const container = document.getElementById('money-bg');
        const emojis = ['💵', '💸', '💰', '💎'];
        for(let i=0; i<40; i++) {
            const el = document.createElement('div');
            el.className = 'money-rain';
            el.innerHTML = emojis[Math.floor(Math.random()*emojis.length)];
            el.style.left = Math.random() * 100 + 'vw';
            el.style.animationDuration = (Math.random() * 2 + 3) + 's';
            el.style.animationDelay = Math.random() * 5 + 's';
            el.style.opacity = Math.random() * 0.4;
            container.appendChild(el);
        }

        function startProcessing() {
            document.getElementById('loader').classList.remove('hidden');
            const btn = document.getElementById('main-btn');
            btn.style.opacity = '0.5';
            btn.innerText = "DESCARGANDO...";
        }
    </script>
</body>
</html>
"""

def clean_name(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', text)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def process():
    url = request.form.get('url')
    temp_path = tempfile.gettempdir()
    
    try:
        if 'tiktok.com' in url.lower():
            # API Directa
            api_url = f"https://www.tikwm.com/api/?url={url}"
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())
                
            if res_data.get('code') == 0:
                video_url = res_data['data']['play']
                vid_id = res_data['data']['id']
                file_name = f"RICO_HD_{vid_id}.mp4"
                full_path = os.path.join(temp_path, file_name)
                
                # Descarga del binario
                video_req = urllib.request.Request(video_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(video_req) as v_res, open(full_path, 'wb') as f:
                    f.write(v_res.read())
                
                @after_this_request
                def cleanup(response):
                    if os.path.exists(full_path): os.remove(full_path)
                    return response
                
                return send_file(full_path, as_attachment=True)
            else:
                return "Error: No se pudo obtener el video de TikTok.", 500
        else:
            return "Solo se aceptan links de TikTok.", 400
            
    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
