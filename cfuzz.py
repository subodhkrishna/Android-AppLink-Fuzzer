from drozer import android
from drozer.modules import common, Module
from urllib import urlencode
from urlparse import parse_qsl, urlparse, urlunparse

cfuzz_wordlist = ["test","afasf","aasdasd"]

class Cfuzz(Module):
	name = "cfuzz"
	description = "Starts an Activity using the formulated intent."
	examples = """
		#TODO: example
		"""
	author = "Phanikar Chereddi (@subodhkrishna @PChereddi1)"
	date = "2019-1-18"
	license = "None"
	path = ["app", "activity"]
	permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

	def add_arguments(self, parser):
		android.Intent.addArgumentsTo(parser)

	def execute(self, arguments):
		intent = android.Intent.fromParser(arguments)


		self.stdout.write("start\n")
		self.stdout.write("DATA URI: "+str(intent.data_uri)+"\n")
		self.stdout.write("ACTION: "+str(intent.action)+"\n")
		self.stdout.write("CATEGORY: "+str(intent.category)+"\n")
		self.stdout.write("COMPONENT: "+str(intent.component)+"\n")
		self.stdout.write("EXTRAS: "+str(intent.extras)+"\n")
		self.stdout.write("FLAGS: "+str(intent.flags)+"\n")
		self.stdout.write("MIME-TYPE: "+str(intent.mimetype)+"\n")
		cfuzz_uri = intent.data_uri
		#parse the custom URI
		try:
			cfuzz_uri_parts = list(urlparse(cfuzz_uri))
		except:
			self.stderr.write("Error parsing the data URI\n")

		cfuzz_uri_query_params = dict(parse_qsl(cfuzz_uri_parts[4]))
		for cfuzz_word in cfuzz_wordlist:
			for key, value in cfuzz_uri_query_params.iteritems():
				cfuzz_uri_query_params[key] = cfuzz_word
				cfuzz_uri_parts[4] = urlencode(cfuzz_uri_query_params)
				updated_uri = urlunparse(cfuzz_uri_parts)
				intent.data_uri = updated_uri
			self.stdout.write("DATA URI: "+str(intent.data_uri)+"\n")
			if len(intent.flags) == 0:
				intent.flags.append('ACTIVITY_NEW_TASK')

			if intent.isValid():
				self.getContext().startActivity(intent.buildIn(self))
			else:
				self.stderr.write("invalid intent: one of action or component must be set\n")