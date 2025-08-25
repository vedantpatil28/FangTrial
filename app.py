from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from datetime import datetime, timedelta
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'blackfang-intelligence-secret-key-2025'

# Demo user data
DEMO_USER = {
    'email': 'demo@blackfangintel.com',
    'password': 'demo123',
    'id': 1,
    'name': 'Demo Automotive Dealership',
    'company_name': 'Demo Motors Pvt Ltd',
    'subscription_plan': 'professional',
    'monthly_fee': 45000
}

# Demo data
COMPETITORS = [
    {
        'id': 1,
        'name': 'AutoMax Dealers',
        'website': 'cars24.com',
        'threat_level': 'HIGH',
        'industry': 'Automotive',
        'location': 'Mumbai, Maharashtra',
        'monitoring_status': 'active',
        'alert_count': 3,
        'last_scraped': datetime.now().isoformat()
    },
    {
        'id': 2,
        'name': 'Speed Motors',
        'website': 'carwale.com',
        'threat_level': 'MEDIUM',
        'industry': 'Automotive',
        'location': 'Delhi, NCR',
        'monitoring_status': 'active',
        'alert_count': 2,
        'last_scraped': datetime.now().isoformat()
    },
    {
        'id': 3,
        'name': 'Elite Auto Solutions',
        'website': 'cardekho.com',
        'threat_level': 'LOW',
        'industry': 'Automotive',
        'location': 'Bangalore, Karnataka',
        'monitoring_status': 'active',
        'alert_count': 3,
        'last_scraped': datetime.now().isoformat()
    }
]

ALERTS = [
    {
        'id': 1,
        'competitor_id': 1,
        'competitor_name': 'AutoMax Dealers',
        'title': '🔴 CRITICAL: Major Price War Detected',
        'severity': 'HIGH',
        'message': 'AutoMax Dealers implemented aggressive 8% price reduction on Honda City models (₹95,000 decrease). Market share impact imminent within 48 hours. Competitive analysis shows this is part of Q4 market expansion strategy.',
        'recommendation': 'IMMEDIATE ACTION: (1) Consider price matching within 24 hours, OR (2) Launch "Premium Service Value" campaign highlighting superior warranty, service quality, and customer support. (3) Activate loyalty program for existing customers. (4) Prepare inventory management for increased demand.',
        'confidence_score': 0.95,
        'created_at': datetime.now().isoformat(),
        'is_read': False
    },
    {
        'id': 2,
        'competitor_id': 2,
        'competitor_name': 'Speed Motors',
        'title': '🟡 STRATEGIC ALERT: Marketing Campaign Launch',
        'severity': 'MEDIUM',
        'message': 'Speed Motors launched comprehensive "Monsoon Festival Special" campaign: 5% additional discount + Free comprehensive insurance + Extended warranty + Zero processing fees. Digital ad spend increased 40% across Facebook, Google, and Instagram.',
        'recommendation': 'STRATEGIC RESPONSE WITHIN 72 HOURS: (1) Deploy "Exclusive Client Benefits" package with comparable or superior value proposition. (2) Leverage social media with customer testimonials. (3) Consider partnership with insurance providers for competitive offering. (4) Activate email marketing to warm leads.',
        'confidence_score': 0.87,
        'created_at': (datetime.now() - timedelta(hours=2)).isoformat(),
        'is_read': False
    },
    {
        'id': 3,
        'competitor_id': 3,
        'competitor_name': 'Elite Auto Solutions',
        'title': '🟡 OPPORTUNITY: Service Quality Issues',
        'severity': 'MEDIUM',
        'message': 'Elite Auto Solutions received 4 negative reviews in past 48 hours citing delivery delays (avg 3 weeks vs promised 1 week), poor after-sales support response times, and parts availability issues. Customer sentiment analysis shows -15% decline.',
        'recommendation': 'COMPETITIVE ADVANTAGE OPPORTUNITY: (1) Launch "Guaranteed Delivery Timeline" campaign with penalty clause for delays. (2) Promote superior after-sales service with same-day response guarantee. (3) Target their dissatisfied customers with "Satisfaction Guarantee" program. (4) Create comparison content highlighting service reliability.',
        'confidence_score': 0.91,
        'created_at': (datetime.now() - timedelta(hours=5)).isoformat(),
        'is_read': False
    },
    {
        'id': 4,
        'competitor_id': 1,
        'competitor_name': 'AutoMax Dealers',
        'title': '🔵 INTELLIGENCE: Inventory Strategy Shift',
        'severity': 'LOW',
        'message': 'AutoMax Dealers updated website with 23% increase in premium SUV listings over past 7 days. New featured categories include luxury segment vehicles. Price positioning suggests targeting higher-income demographics.',
        'recommendation': 'STRATEGIC PREPARATION: (1) Review current SUV inventory levels and pricing strategy. (2) Analyze customer data for luxury segment demand in your market. (3) Consider expanding premium vehicle offerings if market data supports. (4) Prepare competitive pricing analysis for luxury segment.',
        'confidence_score': 0.78,
        'created_at': (datetime.now() - timedelta(hours=8)).isoformat(),
        'is_read': True
    },
    {
        'id': 5,
        'competitor_id': 2,
        'competitor_name': 'Speed Motors',
        'title': '🔵 MONITORING: Enhanced Digital Presence',
        'severity': 'LOW',
        'message': 'Speed Motors expanded digital marketing footprint: 40% increase in social media advertising spend, new video marketing campaign launched, website traffic up 25% (estimated). Enhanced SEO efforts detected with new content strategy.',
        'recommendation': 'DIGITAL STRATEGY EVALUATION: (1) Assess current digital marketing budget allocation vs competition. (2) Consider enhanced social media engagement strategy. (3) Evaluate video marketing opportunities for showroom tours, customer testimonials. (4) Review SEO strategy and content calendar.',
        'confidence_score': 0.82,
        'created_at': (datetime.now() - timedelta(hours=12)).isoformat(),
        'is_read': True
    }
]

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        
        if email == DEMO_USER['email'] and password == DEMO_USER['password']:
            session['user_id'] = DEMO_USER['id']
            session['user_email'] = DEMO_USER['email']
            session['user_name'] = DEMO_USER['name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Calculate statistics
    total_competitors = len(COMPETITORS)
    active_competitors = len([c for c in COMPETITORS if c['monitoring_status'] == 'active'])
    total_alerts = len(ALERTS)
    unread_alerts = len([a for a in ALERTS if not a['is_read']])
    high_priority_alerts = len([a for a in ALERTS if a['severity'] == 'HIGH'])
    
    stats = {
        'total_competitors': total_competitors,
        'active_competitors': active_competitors,
        'total_alerts': total_alerts,
        'unread_alerts': unread_alerts,
        'high_priority_alerts': high_priority_alerts,
        'monitoring_status': '24/7 Active'
    }
    
    return render_template('dashboard.html', 
                         user=session, 
                         stats=stats, 
                         alerts=ALERTS[:3], 
                         competitors=COMPETITORS)

@app.route('/competitors')
def competitors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('competitors.html', 
                         user=session, 
                         competitors=COMPETITORS)

@app.route('/alerts')
def alerts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('alerts.html', 
                         user=session, 
                         alerts=ALERTS)

@app.route('/api/dashboard-data')
def api_dashboard_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'competitors': COMPETITORS,
        'alerts': ALERTS,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/refresh-data')
def api_refresh_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Simulate data refresh by updating timestamps
    for competitor in COMPETITORS:
        competitor['last_scraped'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'message': 'Intelligence data refreshed successfully',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)