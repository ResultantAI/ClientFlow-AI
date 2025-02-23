from flask import Flask, request, jsonify
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class ICPEngine:
    def __init__(self, technographic_data, payment_history, company_size):
        self.stack_compatibility = np.array([0.8, 0.9, 0.85])  # Example compatibility vector
        self.payment_risk = {"example.com": 0.2}  # Example risk score mapping
        self.company_size_weight = self.get_company_size_weight(company_size)  # New company size factor

    def get_company_size_weight(self, company_size):
        """Assigns a weight based on company size for better scoring."""
        if company_size < 10:
            return 0.6  # Small startup
        elif company_size < 100:
            return 0.8  # Mid-size business
        else:
            return 1.0  # Enterprise

    def calculate_icp_score(self, client_data):
        try:
            # Ensure stack is properly formatted as a NumPy array
            stack_array = np.array(client_data.get('stack', [0.5, 0.5, 0.5])).reshape(1, -1)
            compatibility_array = np.array(self.stack_compatibility).reshape(1, -1)

            tech_match = cosine_similarity(stack_array, compatibility_array)[0][0]
            risk_adjustment = 1 - self.payment_risk.get(client_data.get('domain', ""), 1)
            
            # New scoring formula incorporating company size
            icp_score = (tech_match * 0.6) + (risk_adjustment * 0.2) + (self.company_size_weight * 0.2)
            return round(icp_score, 4)

        except Exception as e:
            return f"Error calculating ICP score: {e}"

def generate_proposal(client_name, industry, icp_score):
    """AI-driven proposal generator based on ICP Score."""
    recommendations = [
        f"Enhance AI adoption for {client_name} with automated scoring.",
        f"Implement lead prioritization for {industry}-specific ICP targets.",
        f"Optimize sales strategy using predictive analytics for better revenue."
    ]

    proposal = {
        "client": client_name,
        "industry": industry,
        "icp_score": icp_score,
        "recommendations": recommendations
    }
    return proposal

@app.route('/score', methods=['POST'])
def score():
    data = request.json

    # Validate required keys
    if not isinstance(data, dict) or 'technographic_data' not in data or 'payment_history' not in data or 'client_data' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    company_size = data.get('number_of_employees', 50)  # Default to mid-size if missing
    engine = ICPEngine(data['technographic_data'], data['payment_history'], company_size)
    score = engine.calculate_icp_score(data['client_data'])

    proposal = generate_proposal(data['client_data'].get('domain', "Unknown Company"), "Tech", score)

    return jsonify({'icp_score': score, 'proposal': proposal})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

