class TsRouter(object):

	def db_for_read(self, model, **hints):
		print model._meta.app_label
		return "default"