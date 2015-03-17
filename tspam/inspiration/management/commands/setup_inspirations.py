from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from inspiration.models import Product

product_urls="""White
http://www.finegardening.com/glossy-abelia-abelia-%C2%A0%C3%97-grandiflora
http://www.finegardening.com/black-cohosh-actaea-racemosa
http://www.finegardening.com/chinese-chives-allium-tuberosum
http://www.finegardening.com/masterwort-astrantia-major
http://www.finegardening.com/mountain-sweet-ceanothus-americanus
http://www.finegardening.com/mountain-bluet-centaurea-montana-%E2%80%98amethyst-snow%E2%80%99
http://www.finegardening.com/cosmos-bipinnatus-cvs
http://www.finegardening.com/deutzia-crenata-var-nakaiana-nikko
http://www.finegardening.com/common-snowdrop-galanthus-nivalis
http://www.finegardening.com/mountain-laurel-kalmia-latifolia-and-cvs
http://www.finegardening.com/casa-blanca-oriental-lily-lilium-casa-blanca
http://www.finegardening.com/flowering-tobacco-nicotiana-sylvestris
http://www.finegardening.com/common-garden-peony-paeonia-lactiflora
http://www.finegardening.com/spiraea-nipponica-%E2%80%98snowmound%E2%80%99
http://www.finegardening.com/japanese-stewartia-stewartia-pseudocamellia
http://www.finegardening.com/great-white-trillium-trillium-grandiflorum
Pink
http://www.finegardening.com/apricot-delight-yarrow-achillea-millefolium-apricot-delight
http://www.finegardening.com/hollyhock-alcea-rosea
http://www.finegardening.com/peruvian-lily-alstroemeria-casablanca
http://www.finegardening.com/japanese-anemone-anemone-%C2%A0%C3%97-hybrida-alice
http://www.finegardening.com/bushy-aster-hardy-aster-aster-dumosus-woods-pink
http://www.finegardening.com/scotch-heather-calluna-vulgaris-spring-torch
http://www.finegardening.com/canna-erebus
http://www.finegardening.com/redbud-cercis-canadensis-lavender-twist%C2%AE
http://www.finegardening.com/daphne-%C2%A0%C3%97-transatlantica-summer-ice
http://www.finegardening.com/cheddar-pink-dianthus-baths-pink
http://www.finegardening.com/bleeding-heart-dicentra-spectabilis
http://www.finegardening.com/wand-flower-gaura-lindheimeri
http://www.finegardening.com/rose-campion-lychnis-coronaria-and-cvs
http://www.finegardening.com/four-oclocks-mirabilis-jalapa
http://www.finegardening.com/surfinia-summer-double-pink-petunia-surfinia-summer-double-pink
http://www.finegardening.com/thyme-thymus-pink-ripple
Orange
http://www.finegardening.com/just-peachy-hummingbird-mint-just-peachy-hyssop-agastache-aurantiaca-just-peachy
http://www.finegardening.com/tangerine-beauty-cross-vine-bignonia-capreolata-tangerine-beauty
http://www.finegardening.com/trumpet-creeper-campsis-radicans
http://www.finegardening.com/orange-peel-cestrum-cestrum-orange-peel
http://www.finegardening.com/star-east-crocosmia-crocosmia-star-east
http://www.finegardening.com/dahlia-bed-head
http://www.finegardening.com/coneflower-echinacea-sundown
http://www.finegardening.com/euphorbia-griffithii-fireglow
http://www.finegardening.com/crown-imperial-fritillaria-imperialis
http://www.finegardening.com/fuchsia-coralle
http://www.finegardening.com/mango-lassi-geum-geum-mango-lassi
http://www.finegardening.com/mexican-fire-bush-hamelia-patens
http://www.finegardening.com/daylily-hemerocallis-brazilian-orange
http://www.finegardening.com/flower-carpet%C2%AE-amber-rosa-var-noa97400a-flower-carpet%C2%AE-amber
http://www.finegardening.com/mexican-sunflower-tithonia-rotundifolia%C2%A0-torch
http://www.finegardening.com/tulip-tulipa-praestans-unicum
Blue
http://www.finegardening.com/blue-storm%E2%84%A2-agapanthus-agapanthus-praecox-orientalis-atiblu
http://www.finegardening.com/blue-beard-caryopteris-%C2%A0%C3%97-clandonensis-worcester-gold
http://www.finegardening.com/bigleaf-hydrangea-hydrangea-macrophylla-nikko-blue
http://www.finegardening.com/blue-phlox-phlox-divaricata-blue-moon
http://www.finegardening.com/dwarf-blue-star-amsonia-montana-short-stack%E2%80%99
http://www.finegardening.com/blue-false-indigo-baptisia-australis
http://www.finegardening.com/serbian-bellflower-campanula-poscharskyana-blue-waterfall
http://www.finegardening.com/camassia-leichtlinii-ssp-suksdorfii-blue-danube
http://www.finegardening.com/solitary-clematis-clematis-integrifolia
http://www.finegardening.com/corydalis-flexuosa-blue-panda
http://www.finegardening.com/delphinium-bluebird
http://www.finegardening.com/cranesbill-geranium-%E2%80%98johnsons-blue%E2%80%99
http://www.finegardening.com/spring-starflower-ipheion-uniflorum
http://www.finegardening.com/iris-pallida-variegata
http://www.finegardening.com/virginia-bluebells-mertensia-pulmonarioides
http://www.finegardening.com/grape-hyacinth-muscari-aucheri-blue-magic
Purple
http://www.finegardening.com/angelonia-angelonia-angustifolia
http://www.finegardening.com/butterfly-bush-buddleia-davidii-black-knight
http://www.finegardening.com/saffron-crocus-crocus-sativus
http://www.finegardening.com/sweet-pea-lathyrus-odoratus-and-cvs
http://www.finegardening.com/plantain-lily-hosta-june
http://www.finegardening.com/english-lavender-lavandula-angustifolia
http://www.finegardening.com/blazing-star-liatris-spicata-kobold
http://www.finegardening.com/catmint-nepeta-little-trudy%E2%84%A2
http://www.finegardening.com/blue-passion-flower-passiflora-caerulea
http://www.finegardening.com/pasque-flower-pulsatilla-vulgaris
http://www.finegardening.com/lilac-sage-salvia-verticillata-purple-rain
http://www.finegardening.com/lambs-ears-stachys-byzantina-silky-fleece
http://www.finegardening.com/cut-leaf-lilac-syringa-%C3%97-laciniata
http://www.finegardening.com/meadow-rue-thalictrum-rochebruneanum-lavender-mist
http://www.finegardening.com/purple-mullein-verbascum-phoeniceum
http://www.finegardening.com/tall-verbena-verbena-bonariensis
Yellow
http://www.finegardening.com/superbells%C2%AE-lemon-slice-calibrachoa-calibrachoa-superbells%C2%AE-lemon-slice
http://www.finegardening.com/columbine-aquilegia-canadensis-corbett
http://www.finegardening.com/gold-angels-trumpets-brugmansia-charles-grimaldi
http://www.finegardening.com/forsythia-forsythia-spp-and-cvs
http://www.finegardening.com/yellow-wax-bells-kirengeshoma-palmata
http://www.finegardening.com/yellow-archangel-lamium-galeobdolon
http://www.finegardening.com/magnolia-magnolia-butterflies
http://www.finegardening.com/daffodil-narcissus-tahiti
http://www.finegardening.com/volcanic-sorrel-oxalis-vulcanicola-zinfandel
http://www.finegardening.com/sticky-jerusalem-sage-phlomis-russeliana
http://www.finegardening.com/azalea-rhododendron-admiral-semmes
http://www.finegardening.com/henry-eilers-sweet-coneflower-rudbeckia-subtomentosa-henry-eilers
http://www.finegardening.com/upright-wild-ginger-saruma-henryi
http://www.finegardening.com/goldenrod-solidago-rugosa-fireworks
http://www.finegardening.com/celandine-poppy-stylophorum-diphyllum
http://www.finegardening.com/indian-cress-tropaeolum-majus-vanilla-berry
Red
http://www.finegardening.com/splendens-bottlebrush-callistemon-citrinus-splendens
http://www.finegardening.com/flowering-quince-chaenomeles-%C2%A0%C3%97-superba-%E2%80%98texas-scarlet%E2%80%99
http://www.finegardening.com/mercury-rising-coreopsis-coreopsis-rosea-mercury-rising
http://www.finegardening.com/totally-tempted%E2%84%A2-cuphea-cuphea-llavea-totally-tempted%E2%84%A2
http://www.finegardening.com/blanket-flower-gaillardia-arizona-sun
http://www.finegardening.com/gladiolus-gladiolus-atom
http://www.finegardening.com/gomphrena-gomphrena%C2%A0haageana-strawberry-fields
http://www.finegardening.com/cardinal-flower-lobelia-cardinalis
http://www.finegardening.com/major-wheeler-honeysuckle-vine-lonicera-sempervirens-major-wheeler
http://www.finegardening.com/ever-red%C2%AE-loropetalum-loropetalum-chinense-chang-nian-hong
http://www.finegardening.com/red-spider-lily-lycoris-radiata
http://www.finegardening.com/poppy-papaver-orientale-flamenco-dancer
http://www.finegardening.com/pelargonium-crystal-palace-gem
http://www.finegardening.com/beardlip-penstemon-penstemon-barbatus
http://www.finegardening.com/egyptian-star-cluster-pentas-lanceolata-new-look-red
http://www.finegardening.com/shrubby-cinquefoil-potentilla-fruticosa-gibsons-scarlet"""

class Command(BaseCommand):
    help = "Setup inspirations."

    def handle(self, *args, **options):
        current_color = None
        for product in product_urls.split("\n"):
            product = product.strip().lower()
            if "http" not in product:
                current_color = product.replace(":", "")
                continue
            r = requests.get(product)
            if r.status_code != 200:
                print "ERROR", "#"*30
            if Product.objects.filter(source_url = product).count() > 0:
                print "Product already exists", product
                continue
            pobj = Product()
            soup = BeautifulSoup(r.content)
            pobj.name = soup.find_all("h2", {"class":"plant-title"})[0].text.strip()
            pobj.color = current_color
            pobj.source_url = product
            pobj.image_url = soup.find_all("h3", {"class":"title-latin-name"})[0].next_sibling.next_sibling.find_all("img")[0]["src"]
            try:
                pobj.description = soup.find_all("div", {"class":"field-name-field-fg-plant-body"})[0].text.strip()
            except:
                pobj.description = ""
            pobj.save()