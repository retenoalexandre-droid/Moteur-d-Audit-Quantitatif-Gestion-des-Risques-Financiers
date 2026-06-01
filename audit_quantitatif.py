import numpy as np
import logging
import yfinance as yf
import matplotlib.pyplot as plt
from typing import List, Dict, Union

# =============================================================================
# CONFIGURATION DU LOGGING
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# BIBLIOTHÈQUE MATHÉMATIQUE (Les Modèles)
# =============================================================================
class RiskManagement:
    """ Module 1 : Survie du Portefeuille et Risque Systémique (2008) """
    
    @staticmethod
    def calculate_expected_shortfall(returns: List[float], confidence_level: float = 0.99) -> Dict[str, float]:
        if not returns:
            raise ValueError("La liste des rendements ne peut pas être vide.")
        if not (0 < confidence_level < 1):
            raise ValueError("Le niveau de confiance doit être strictement compris entre 0 et 1.")

        returns_array = np.array(returns)
        var_threshold = float(np.percentile(returns_array, (1 - confidence_level) * 100))
        
        extreme_losses = returns_array[returns_array <= var_threshold]
        expected_shortfall = float(extreme_losses.mean()) if extreme_losses.size > 0 else var_threshold
        
        return {"VaR": var_threshold, "Expected_Shortfall": expected_shortfall}

    @staticmethod
    def basel_iii_stress_test(assets: float, equity_ratio: float, crash_severity: float) -> Dict[str, Union[bool, float]]:
        if assets <= 0 or equity_ratio < 0 or crash_severity < 0:
            raise ValueError("Les actifs, le ratio et la sévérité doivent être des valeurs positives.")

        equity_capital = assets * equity_ratio
        loss = assets * crash_severity
        surviving_equity = equity_capital - loss
        is_bankrupt = surviving_equity < 0
        
        if is_bankrupt:
            logger.warning(f"Banque insolvable. Pertes ({loss:,.0f}$) > Fonds propres ({equity_capital:,.0f}$)")
        
        return {
            "Bailout_Required": is_bankrupt,
            "Remaining_Equity": max(0.0, surviving_equity)
        }

class AlgorithmicSafeguards:
    """ Module 2 : Sécurité Haute Fréquence (Flash Crash 2010) """

    @staticmethod
    def circuit_breaker_luld(current_price: float, reference_price: float, tolerance_pct: float = 0.10) -> str:
        upper_limit = reference_price * (1 + tolerance_pct)
        lower_limit = reference_price * (1 - tolerance_pct)
        
        if current_price > upper_limit or current_price < lower_limit:
            msg = f"COUPE-CIRCUIT ACTIVÉ. Le prix ({current_price:.2f}$) est hors tolérance."
            logger.error(msg)
            return "ALERTE"
            
        return "NORMAL"

class CorporateValuation:
    """ Module 3 : Private Equity & Fondamentaux (Bulle Dot-com & DCF) """

    @staticmethod
    def present_value_dcf(future_cash_flow: float, discount_rate: float, years_in_future: int) -> float:
        present_value = future_cash_flow / ((1 + discount_rate) ** years_in_future)
        return round(float(present_value), 2)

    @staticmethod
    def cash_burn_trajectory(initial_cash: float, margin_per_unit: float, volume_array: List[int]) -> List[float]:
        cash_levels = [float(initial_cash)]
        
        for step, volume in enumerate(volume_array):
            new_cash = cash_levels[-1] + (margin_per_unit * volume)
            cash_levels.append(float(new_cash))
            
            if new_cash <= 0:
                logger.critical(f"FAILLITE MATHÉMATIQUE ATTEINTE à l'étape {step + 1} (Trésorerie: {new_cash}$).")
                break
                
        return cash_levels

# =============================================================================
# FONCTION DE VISUALISATION GRAPHIQUE
# =============================================================================
def plot_financial_graphics(cash_trajectory: List[float], returns: List[float], var_threshold: float):
    """ Génère des graphiques professionnels pour le README ou le portfolio """
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Graphique 1 : Trajectoire de Cash Burn
    ax1.plot(cash_trajectory, marker='o', color='firebrick', linewidth=2, label='Solde Trésorerie')
    ax1.axhline(0, color='black', linestyle='--', linewidth=1.2)
    ax1.set_title("Évolution de la Trésorerie (Scénario Cash Burn)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Étapes de Scaling (Volume croissant)")
    ax1.set_ylabel("Cash disponible ($)")
    ax1.legend()
    
    # Graphique 2 : Histogramme des rendements et VaR
    ax2.hist(returns, bins=40, color='dodgerblue', alpha=0.7, edgecolor='black', label='Rendements Réels')
    ax2.axvline(var_threshold, color='red', linestyle='--', linewidth=2, label=f'VaR Seuil ({var_threshold:.2%})')
    ax2.set_title("Distribution des Rendements & Seuil de Risque (VaR)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Rendements Quotidiens")
    ax2.set_ylabel("Fréquence (Jours)")
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

# =============================================================================
# ZONE D'EXÉCUTION (LE CRASH-TEST AVEC DONNÉES RÉELLES)
# =============================================================================
if __name__ == "__main__":
    logger.info("=== DÉMARRAGE DE L'AUDIT QUANTITATIF (LIVE DATA) ===")

    # ---------------------------------------------------------
    # MODULE 1 : YFINANCE & RISQUE DE MARCHÉ
    # ---------------------------------------------------------
    ticker_symbol = "TSLA" 
    logger.info(f"[MODULE 1A] Téléchargement des données pour {ticker_symbol} (1 dernière année)...")
    
    try:
        market_data = yf.download(ticker_symbol, period="1y", progress=False)
        
        if market_data.empty:
            raise ValueError(f"Impossible de récupérer les données pour {ticker_symbol}.")

        real_returns = market_data['Close'].pct_change().dropna().iloc[:, 0].tolist()
        derniers_prix = market_data['Close'].iloc[-1, 0] 
        
        logger.info(f" -> {len(real_returns)} jours de trading analysés. Prix actuel : {derniers_prix:.2f}$")

        resultat_risque = RiskManagement.calculate_expected_shortfall(real_returns, confidence_level=0.95)
        
        logger.info(f" -> Value at Risk (VaR 95%) : {resultat_risque['VaR']:.2%} (Pire perte quotidienne 'normale')")
        logger.info(f" -> Expected Shortfall (ES 95%) : {resultat_risque['Expected_Shortfall']:.2%} (Moyenne du gouffre)")

        # ---------------------------------------------------------
        # MODULE 1B : BÂLE III AVEC LE VRAI ES
        # ---------------------------------------------------------
        logger.info("\n[MODULE 1B] Stress Test Bâle III (Basé sur le choc réel)")
        crash_severity = abs(resultat_risque['Expected_Shortfall'])
        
        resultat_banque = RiskManagement.basel_iii_stress_test(
            assets=10_000_000, 
            equity_ratio=0.08, 
            crash_severity=crash_severity
        )
        logger.info(f" -> Plan de sauvetage requis ? {'OUI' if resultat_banque['Bailout_Required'] else 'NON'}")
        logger.info(f" -> Fonds propres restants après le crash : {resultat_banque['Remaining_Equity']:,.0f} $")

        # ---------------------------------------------------------
        # MODULE 2 : SÉCURITÉ HFT 
        # ---------------------------------------------------------
        logger.info("\n[MODULE 2] Sécurité Haute Fréquence (Flash Crash simulé)")
        prix_hft_fou = derniers_prix * 0.85
        AlgorithmicSafeguards.circuit_breaker_luld(
            current_price=prix_hft_fou, 
            reference_price=derniers_prix, 
            tolerance_pct=0.10
        )

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse boursière : {e}")

    # ---------------------------------------------------------
    # MODULE 3 : VALORISATION
    # ---------------------------------------------------------
    logger.info("\n[MODULE 3] Valorisation DCF & Cash Burn")
    valeur_reelle = CorporateValuation.present_value_dcf(future_cash_flow=10_000_000, discount_rate=0.10, years_in_future=5)
    logger.info(f" -> DCF : Valeur actuelle de 10M€ dans 5 ans : {valeur_reelle:,.2f} €")
    
    # Récupération des données et exécution du tracé de Cash Burn
    trajectoire = CorporateValuation.cash_burn_trajectory(initial_cash=50000, margin_per_unit=-2.5, volume_array=[1000, 5000, 15000, 50000])
    
    logger.info("\n[VISUALISATION] Génération des graphiques d'analyse...")
    plot_financial_graphics(cash_trajectory=trajectoire, returns=real_returns, var_threshold=resultat_risque['VaR'])
    
    logger.info("=== FIN DE L'AUDIT ===")
