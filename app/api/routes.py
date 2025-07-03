from flask import request, jsonify, Blueprint, current_app
from . import api_bp
from app.services import AIService, JiraService
from app.services.summary_generator import generate_summary
import io

@api_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    print(f"---Health Checking Status: Ok!")
    return jsonify({"status": "ok"}), 200

@api_bp.route('/create_jira_story', methods=['POST'])
def create_jira_story_endpoint():
    data = request.get_json()
    if not data or 'prompt' not in data or 'project_key' not in data or 'type' not in data or 'asigned_to' not in data:
        print(f"\033[91mRequest body must contain 'prompt', 'project_key', 'type', and 'asigned_to'\033[0m")
        return jsonify({"error": "Request body must contain 'prompt', 'project_key', 'type', and 'asigned_to'"}), 400

    try:
        issue_type = data['type'].lower()
        if issue_type not in ['story', 'bug']:
            return jsonify({'error': "Invalid 'type'. Must be 'story' or 'bug'."}), 400
        
        if len(data['prompt']) < 50:
            print(f"\033[91mPrompt must be at least 50 characters long\033[0m")
            return jsonify({"error": "Prompt must be at least 50 characters long"}), 400

        # Initialize services
        ai_service = AIService(api_key=current_app.config['GOOGLE_API_KEY'])
        jira_service = JiraService(
            server=current_app.config['JIRA_SERVER'],
            username=current_app.config['JIRA_USERNAME'],
            api_token=current_app.config['JIRA_API_TOKEN']
        )

        # 1. Generate issue details with AI
        issue_details = ai_service.generate_jira_issue_details(data['prompt'], issue_type)

        # 2. Create JIRA Issue
        asigned_to = data.get('asigned_to')
        parentId = data.get('parent_id')
        issue_key = jira_service.create_jira_issue(data['project_key'], issue_type, issue_details, asigned_to, parentId)
        story_points = 8
        jira_service.update_story_points(issue_key, story_points)
        return jsonify({
            "success": True,
            "status": 200,
            "data": {"message": f"JIRA {issue_type} created successfully!", "issue_key": issue_key}
        })

    except (ValueError, RuntimeError, ConnectionError) as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred: {e}\033[0m")
        return jsonify({"error": "An internal server error occurred."}), 500

# api_bp.register_blueprint(review_bp)


@api_bp.route('/review', methods=['POST'])
def review_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "status": 400, "data": {"error": "No file part"}}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "status": 400, "data": {"error": "No selected file"}}), 400

    if file:
        try:
            file_stream = io.BytesIO(file.read())
            summary = generate_summary(file_stream, file.mimetype)
            
            if "Unsupported file type" in summary:
                 return jsonify({"success": False, "status": 415, "data": {"content_summary": summary}}), 415
            
            if "Could not extract text" in summary:
                return jsonify({"success": False, "status": 422, "data": {"content_summary": summary}}), 422

            if "Failed to generate summary" in summary:
                 return jsonify({"success": False, "status": 500, "data": {"content_summary": summary}}), 500

            response_data = {
                "success": True,
                "status": 200,
                "data": {
                    "content_summary": summary
                }
            }
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({"success": False, "status": 500, "data": {"error": str(e)}}), 500

    return jsonify({"success": False, "status": 500, "data": {"error": "An unknown error occurred"}}), 500 
