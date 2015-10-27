__author__ = 'luissaguas'


from frappe.celery_app import celery_task
import frappe

pubsub = None


def publish(channel, message):
	from frappe.async import get_redis_server

	r = get_redis_server()
	r.publish(channel, message)


def get_redis_pubsub():
	from frappe.async import get_redis_server

	global pubsub
	if not pubsub:
		r = get_redis_server()
		pubsub = r.pubsub()
	return pubsub


def subscribe(*args, **kwargs):
	p = get_redis_pubsub()
	p.subscribe(*args, **kwargs)


def run_async_task(site):
	#from l10n_pt_hr_salary.tasks import get_message

	#print "running async task"
	x = X()
	#task = x.get_message.delay(site)
	x.delay(site)
	#print "saguas task %s" % task.id


def get_messages():
	p = get_redis_pubsub()
	return p.get_message()
#print "prepare for messages for redis pubsub"
#run_async_task()
#subscribe("teste_channel")
#publish("teste_channel", "ola saguas")

#from celery.contrib.methods import task

from celery import Task
#from celery.contrib.methods import task_method

class X(Task):
#class X(object):
#@celery_task()
	#@task()
	#@current_app.task(filter=task_method)

	def run(self, site):
		self.get_message(site)

	#@current_app.task(filter=task_method)
	def get_message(self, site):
		#from l10n_pt_hr_salary.utils.utils import get_redis_pubsub
		#from l10n_pt_hr_salary import get_redis_pubsub
		#import time
		frappe.init(site=site)
		p = get_redis_pubsub()
		subscribe("teste_channel")
		from frappe.async import emit_via_redis
		#print "waiting from message from redis %s" % p
		for message in p.listen():
			print "saguas message %s" % message
			response = {}
			response.update({
				"status": "Success",
				"task_id": "yowsub",
				"result": "ola from python"
			})
			emit_via_redis("teste_channel2", response, "task:yowsub")

		#while True:
		#	message = p.get_message()
		#	if message:
		#		print "message %s" % message
		#	time.sleep(0.001)  # be nice to the system :)


#run_async_task("site2.local")