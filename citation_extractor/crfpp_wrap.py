"""
Creates a wrapper around the CRF++ implementation.
"""

import CRFPP
import sys
import logging
import os
#import pprint

def train_crfpp(template_file,train_data_file,model_file):
		cmd="crf_learn -f 1 -t %s %s %s"%(template_file,train_data_file,model_file)
		logger = logging.getLogger('CREX.TRAIN_CRFPP')
		logger.info(cmd)
		os.popen(cmd).readlines()
		return

class CRF_classifier:
	def __init__(self,model_file,verb_level=2,best_out_n=2):
		self.logger = logging.getLogger('CREX.CRFPP_WRAP.CRFPP')
		try:
			self.m,self.v,self.bn=model_file,verb_level,best_out_n
			self.tagger = CRFPP.Tagger("-m %s -v %i -n%i"%(model_file,verb_level,best_out_n))
			self.logger.info("CRFPP Tagger initialized with command %s"%("-m %s -v %i -n%i"%(self.m,self.v,self.bn)))
		except RuntimeError, e:
			print "RuntimeError: ", e,
	def __getstate__(self):
		odict = self.__dict__.copy()
		del odict['tagger']
		return odict
	def __setstate__(self,dict):
		self.__dict__.update(dict)
		self.tagger = CRFPP.Tagger("-m %s -v %i -n%i"%(self.m,self.v,self.bn))
		print "CRFPP Tagger initialized with command %s"%("-m %s -v %i -n%i"%(self.m,self.v,self.bn))
	
	def classify(self,l_tokens):
		"""
		Classify a lost of tokens.
		
		Args:
			l_tokens: A list of string where the token and its feature vector are separated by tabs ("\t").
			
			For example: an instance with tokens ("Eschilo","interprete") would correspond to the following list
			[
			u'Eschilo\tOTHERS\tINIT_CAPS\teschilo\tNO_DIGITS\tOTHERS\t7\tE\tEs\tEsc\tEsch\to\tlo\tilo\thilo'
			, u'interprete\tOTHERS\tALL_LOWER\tinterprete\tNO_DIGITS\tOTHERS\t10\ti\tin\tint\tinte\te\tte\tete\trete'
			]
		"""
		#self.logger.debug("%s##"%l_tokens)
		out=[]
		self.tagger.clear()
		for t in l_tokens:
			t=t.encode("utf-8")
			self.tagger.add(t.decode("string-escape"))
		self.tagger.parse()
		size = self.tagger.size()
		xsize = self.tagger.xsize()
		ysize = self.tagger.ysize()
		for i in range(0, (size)):
		   res={}
		   feats=[]
		   res['id']=i+1
		   for j in range(0, (xsize)):
			if(j==0):
				res['token']=self.tagger.x(i, j)
			else:
				feats.append(self.tagger.x(i, j))
			res['features']=feats
		   self.logger.debug(res['features'])
		   res['label']=self.tagger.y2(i)
		   res['probs']={}
		   for j in range(0, (ysize)):
			tag=self.tagger.yname(j)
			probs={}
			vals = (float(self.tagger.prob(i,j)),float(self.tagger.alpha(i, j)),float(self.tagger.beta(i, j)))
			probs['prob']="%f"%vals[0]
			probs['alpha']="%f"%vals[1]
			probs['beta']="%f"%vals[2]
			res['probs'][tag]=probs
		   self.logger.debug("%s => %s (%s)"%(res["token"].decode("utf-8"),res["label"].decode("utf-8"),str(res["probs"][res["label"]]['prob'])))
		   out.append(res)
		return out
	

if __name__ == "__main__":
    # crf_learn -t /56k/phd/code/python/crfx.tpl /56k/phd/code/python/doc1.train /56k/phd/code/python/crfx.mdl
    train_crfpp("/56k/phd/code/python/crfx.tpl","/56k/phd/code/python/doc1.train","/56k/phd/code/python/eval/new.mdl")
			