#coding:utf-8
from cactus.deployment.neocities.rest.abstract import NeocitiesRestAbstract

class NeocitiesList(NeocitiesRestAbstract):
    Action = "list"
    Method = "GET"
    
 