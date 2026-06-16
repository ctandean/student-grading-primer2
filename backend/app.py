from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
 
    if not student_data:
        return error("Request body must be JSON")
 
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", None)
 
    if not name or not isinstance(name, str):
        return jsonify({"error": "invalid name"}), 404
 
    if not course or not isinstance(course, str):
        return jsonify({"error": "invalid course"}), 404
 
    if mark is not None:
        if not isinstance(mark, (int, float)) or not (0 <= mark <= 100):
            return jsonify({"error": "invalid mark"}), 404
 
    student = db.insert_student(name, course, mark)
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    existing = db.get_student_by_id(student_id)
    if existing is None:
        return jsonify({"error": "student does not exist"}), 404

    student_data = request.json
    if not student_data:
        return jsonify({"error": "failed to get student data"}), 404

    name = student_data.get("name", existing["name"])
    course = student_data.get("course", existing["course"])
    mark = student_data.get("mark", existing["mark"])

    if not name or not isinstance(name, str):
        return jsonify({"error": "invalid name"}), 404

    if not course or not isinstance(course, str):
        return jsonify({"error": "invalid course"}), 404

    if mark is not None:
        if not isinstance(mark, (int, float)) or not (0 <= mark <= 100):
            return jsonify({"error": "invalid mark"}), 404

    updated = db.update_student(student_id, name, course, mark)
    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({"error": "student does not exist"}), 404
 
    db.delete_student(student_id)
    return jsonify(student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [s["mark"] for s in students if s.get("mark") is not None]
 
    if not marks:
        return jsonify({
            "count": 0,
            "average": None,
            "min": None,
            "max": None
        }), 200
 
    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
