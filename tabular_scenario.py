from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_france import CountryTaxBenefitSystem
from openfisca_france.model.base import Famille, FoyerFiscal, Menage
import pandas as pd

class StrasbourgSurveyScenario(AbstractSurveyScenario):
    def __init__(self, data = None):
        super(StrasbourgSurveyScenario, self).__init__()

        tax_benefit_system = CountryTaxBenefitSystem()
        tax_benefit_system.load_extension('openfisca_france_local')

        input_data_frame = data.get('input_data_frame')
        self.used_as_input_variables = list(
            set(tax_benefit_system.variables.keys()).intersection(
                set(input_data_frame.columns)
                ))

        self.set_tax_benefit_systems(tax_benefit_system)
        self.year = "2021-03"
        self.init_from_data(data = data)

qf = [410, 510, 620, 720, 820, 920, 1030, 1540, 2050, 2051, 2052]
counts = [4025, 2113, 1832, 1603, 962, 638, 566, 1990, 1157, 2090, 45]

input_data_frame = pd.DataFrame({
    'strasbourg_metropole_quotient_familial': qf,
    'famille_role_index': 0,
    'foyer_fiscal_role_index': 0,
    'menage_role_index': 0,
    'famille_id': range(len(qf)),
    'foyer_fiscal_id': range(len(qf)),
    'menage_id': range(len(qf)),
    })

data = dict(input_data_frame = input_data_frame)
scenario = StrasbourgSurveyScenario(data = data)

tarif_cantine = scenario.simulation.calculate('strasbourg_metropole_tarification_cantine', period = '2021-03')

sum_tranches = counts * tarif_cantine * 200 # Pour 200 repas par an
print('vecteur des recettes par tranche')
print(sum_tranches)

print('recettes totales')
print(sum(sum_tranches))
