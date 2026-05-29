import kagglehub
import pandas as pd
import numpy as np
import os
from scipy.stats import beta

def main():
    # 1. Download the dataset
    print("Downloading dataset from Kaggle...")
    dataset_path = kagglehub.dataset_download("justinlimyin/hr-employee-dataset")
    
    # List files to find the CSV
    csv_file = None
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".csv"):
                csv_file = os.path.join(root, file)
                break
        if csv_file:
            break
            
    if not csv_file:
        print("No CSV file found in the dataset.")
        return

    print(f"Loading dataset from: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"Original dataset shape: {df.shape}")

    # 2. Generate synthetic cases until 5,000 unique IDs
    target_records = 5000
    current_records = len(df)
    
    if current_records < target_records:
        print(f"Generating {target_records - current_records} synthetic records...")
        
        additional_records = target_records - current_records
        synthetic_df = df.sample(n=additional_records, replace=True).copy()
        
        # We'll create a new Employee_ID column to ensure uniqueness
        synthetic_df['Employee_ID_Custom'] = range(current_records + 1, target_records + 1)
        df['Employee_ID_Custom'] = range(1, current_records + 1)
        
        # Add some noise to numerical columns to avoid exact duplicates
        for col in synthetic_df.select_dtypes(include=[np.number]).columns:
            if col != 'Employee_ID_Custom':
                std = df[col].std()
                if std > 0:
                    noise = np.random.normal(0, std * 0.05, size=len(synthetic_df))
                    synthetic_df[col] = synthetic_df[col] + noise
        
        df = pd.concat([df, synthetic_df], ignore_index=True)

    # 3. Simulate PCI training result (resultado_capacitacion_pci)
    print("Simulating PCI training results...")
    
    # Seleccionar features para la regresión (excluyendo IDs)
    feature_cols = [col for col in df.columns if col not in ['Employee_ID', 'Employee_ID_Custom']]
    
    # Codificar variables categóricas
    from sklearn.preprocessing import LabelEncoder
    df_encoded = df[feature_cols].copy()
    le = LabelEncoder()
    for col in df_encoded.select_dtypes(include=['object']).columns:
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
    
    # Generar coeficientes aleatorios para la regresión
    np.random.seed(42)
    coefficients = np.random.randn(len(feature_cols))
    
    # Calcular predicción base
    prediction = np.dot(df_encoded.values, coefficients)
    
    # Normalizar y escalar a rango apropiado con media 90
    # Para sesgo a la izquierda, usar distribución beta invertida
    
    # Normalizar predicciones a [0, 1]
    prediction_normalized = (prediction - prediction.min()) / (prediction.max() - prediction.min())
    
    # Aplicar transformación beta para sesgo a la izquierda (alpha > beta)
    # Con alpha=8, beta=2 obtenemos sesgo a la izquierda
    beta_transformed = beta.ppf(prediction_normalized, a=8, b=2)
    
    # Escalar a rango [50, 100] con media aproximada de 90
    df['resultado_capacitacion_pci'] = 50 + (beta_transformed * 50)
    
    # Ajustar para asegurar media de 90
    current_mean = df['resultado_capacitacion_pci'].mean()
    df['resultado_capacitacion_pci'] = df['resultado_capacitacion_pci'] + (90 - current_mean)
    
    # Asegurar que valores estén en rango [50, 100]
    df['resultado_capacitacion_pci'] = df['resultado_capacitacion_pci'].clip(50, 100)
    
    # Redondear a enteros
    df['resultado_capacitacion_pci'] = df['resultado_capacitacion_pci'].round().astype(int)

    # 4. Save to data/dataset_entrada.csv
    output_path = os.path.join("../data", "dataset_entrada.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}. Total records: {len(df)}")
    print("First 5 records:")
    print(df.head())

if __name__ == "__main__":
    main()
