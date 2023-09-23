
# Generics
import all_barrierbuster
import all_daggerthrow
import all_featherpin
import all_fireball
import all_holyamulet
import all_leafcrystal
import all_poisondust
import all_shimmeringstars
import all_stardust
import all_spiritbreak
import all_weakeningamulet

# Healing
import all_healingdrop

# Support
import all_encourage
import all_illusionveil
import all_lifebless
import all_magicalbarrier
import all_physicalbarrier
import all_trackingshot

# SC
import alice_dolls
import aya_tornado
import chen_pentagramflight
import keine_sunbeammirror
import marisa_masterspark
import misaki_curse
import misaki_fire
import mokou_phoenix
import nitori_fireworks
import ran_princesstenko
import reimu_fantasyseal
import youmu_ao
import reisen_ifm
import kaguya_mysterium
import eirin_astral
import ayaka_spear
import haruna_evergreen
import kotone_meteor
import miu_butterfly
import ayaka_lastword
import yukari_ran_and_chen
import yuyuko_resurrectionbutterfly
import fuzzball_swarm
import asa_reflectedtemenos
import fuyuhana_cloudsandsun
import fuyuhana_mightytree
import fuyuhana_iwanagaashes
import tsubaki_redfeathers
import sakuya_killingdoll

# Special
import special_revive
import special_barrier

def get_catalog():
    # This is a list of all bullet scripts available
    catalog = {
               # Spell Actions
               'all_barrierbuster': all_barrierbuster.Script,
               'all_daggerthrow': all_daggerthrow.Script,
               'all_featherpin': all_featherpin.Script,
               'all_fireball': all_fireball.Script,
               'all_holyamulet': all_holyamulet.Script,
               'all_leafcrystal': all_leafcrystal.Script,
               'all_poisondust': all_poisondust.Script,
               'all_shimmeringstars': all_shimmeringstars.Script,
               'all_spiritbreak': all_spiritbreak.Script,
               'all_stardust': all_stardust.Script,
               'all_weakeningamulet': all_weakeningamulet.Script,

               # Healing Spells
               'all_healingdrop': all_healingdrop.Script,

               # Support Spells
               'all_encourage': all_encourage.Script,
               'all_illusionveil': all_illusionveil.Script,
               'all_lifebless': all_lifebless.Script,
               'all_magicalbarrier': all_magicalbarrier.Script,
               'all_physicalbarrier': all_physicalbarrier.Script,
               'all_trackingshot': all_trackingshot.Script,

               # Spell Cards
               'aya_tornado':  aya_tornado.Script,
               'alice_dolls':  alice_dolls.Script,
               'chen_pentagramflight': chen_pentagramflight.Script,
               'keine_sunbeammirror': keine_sunbeammirror.Script,
               'marisa_masterspark': marisa_masterspark.Script,
               'misaki_curse': misaki_curse.Script,
               'misaki_fire': misaki_fire.Script,
               'mokou_phoenix': mokou_phoenix.Script,
               'nitori_fireworks': nitori_fireworks.Script,
               'ran_princesstenko': ran_princesstenko.Script,
               'reimu_fantasyseal': reimu_fantasyseal.Script,
               'youmu_ao': youmu_ao.Script,
               'reisen_ifm':reisen_ifm.Script,
               'kaguya_mysterium':kaguya_mysterium.Script,
               'eirin_astral':eirin_astral.Script,
               'ayaka_spear':ayaka_spear.Script,
               'haruna_evergreen':haruna_evergreen.Script,
               'kotone_meteor':kotone_meteor.Script,
               'miu_butterfly':miu_butterfly.Script,
               'ayaka_lastword':ayaka_lastword.Script,
               'yukari_ran_and_chen':yukari_ran_and_chen.Script,
               'yuyuko_resurrectionbutterfly': yuyuko_resurrectionbutterfly.Script,
               'fuzzball_swarm': fuzzball_swarm.Script,
               'asa_reflectedtemenos':asa_reflectedtemenos.Script,
               'fuyuhana_cloudsandsun':fuyuhana_cloudsandsun.Script,
               'fuyuhana_mightytree':fuyuhana_mightytree.Script,
               'fuyuhana_iwanagaashes':fuyuhana_iwanagaashes.Script,
               'tsubaki_redfeathers':tsubaki_redfeathers.Script,
               'sakuya_killingdoll':sakuya_killingdoll.Script,

               # Special counterbomb animation
               'special_revive': special_revive.Script,
               'special_barrier': special_barrier.Script

               }
    return catalog
