import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=('job', 'team_leader')) for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif session.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    # noinspection PyArgumentList
    job = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('job', 'team_leader'))
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    job.job = request.json['job']
    job.team_leader = request.json['team_leader']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    session.merge(job)
    session.commit()
    return jsonify({'success': 'OK'})
