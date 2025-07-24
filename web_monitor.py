"""
Servidor web simple para monitoreo con UptimeRobot
Solo para verificar que el bot está funcionando
"""
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Endpoint de salud para UptimeRobot"""
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                "status": "online",
                "bot": "Discord Suggestions Bot",
                "timestamp": datetime.now().isoformat(),
                "uptime": "running",
                "version": "1.0.0"
            }
            
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Silenciar logs del servidor web"""
        pass

def start_monitor_server():
    """Inicia el servidor de monitoreo en un hilo separado"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), MonitorHandler)
    
    def run_server():
        print(f"🌐 Monitor web iniciado en puerto {port}")
        server.serve_forever()
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print(f"✅ Servidor de monitoreo disponible en: http://localhost:{port}/health")

if __name__ == "__main__":
    start_monitor_server()
    # Mantener el hilo principal vivo
    try:
        while True:
            import time
            time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 Servidor de monitoreo detenido")