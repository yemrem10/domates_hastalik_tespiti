import streamlit as st
import torch
from torchvision import transforms, models
from PIL import Image
import sqlite3
import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

def get_disease_info(hastalik_adi):
    conn = sqlite3.connect('hastaliklar.db')
    cursor = conn.cursor()
    cursor.execute("SELECT neden, onlem FROM bilgiler WHERE hastalik_adi=?", (hastalik_adi,))
    result = cursor.fetchone() 
    conn.close()
    return result 

def load_model():
    model = models.efficientnet_b0(weights=None)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(num_ftrs, 8) 
    model.load_state_dict(torch.load("egitilmis_en_iyi_model_v2.pth", map_location=torch.device('cpu')))
    model.eval()
    return model


model = load_model()

def predict_and_generate_cam(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(image).unsqueeze(0)
    
  
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted = torch.max(probabilities, 0)
        class_idx = predicted.item()
        conf_score = confidence.item()

    target_layers = [model.features[-1]]

    cam = GradCAM(model=model, target_layers=target_layers)

    targets = [ClassifierOutputTarget(class_idx)]

    grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
    grayscale_cam = grayscale_cam[0, :] 

    rgb_img = Image.open(uploaded_file).convert('RGB')
    transform_for_cam = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
    ])
    rgb_img_cropped = np.float32(transform_for_cam(rgb_img)) / 255
    
    visualization = show_cam_on_image(rgb_img_cropped, grayscale_cam, use_rgb=True, image_weight=0.7)
    
    return class_idx, conf_score, visualization


st.title("🍅 Domates Hastalığı Tespit Sistemi", anchor=False)

st.markdown("<br><br><br>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Bir yaprak fotoğrafı seçin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    original_image = Image.open(uploaded_file)
    
    with st.spinner('Yapay zeka analiz ediyor ve ısı haritasını oluşturuyor...'):
        label_idx, confidence, cam_visualization = predict_and_generate_cam(original_image)
    
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        st.subheader("Orijinal Fotoğraf", anchor=False)

        st.image(original_image, caption='Yüklenen Fotoğraf', width='stretch')
        
    with img_col2:
        st.subheader("Isı Haritası", anchor=False)

        st.image(cam_visualization, caption='Modelin Odaklandığı Bölgeler', width='stretch')
 
    st.markdown("<br>", unsafe_allow_html=True)
    class_names = ["Erken Yanıklık", "Sağlıklı", "Geç Yanıklık", "Yaprak Galeri Sineği", "Magnezyum Eksikliği", "Azot Eksikliği", "Potasyum Eksikliği", "Lekeli Solgunluk Virüsü"] 
    result_label = class_names[label_idx]
    confidence_percentage = f"%{confidence * 100:.1f}"
    
    yellow_alerts = ["Magnezyum Eksikliği", "Azot Eksikliği", "Potasyum Eksikliği"]
    red_alerts = ["Erken Yanıklık", "Geç Yanıklık", "Yaprak Galeri Sineği", "Lekeli Solgunluk Virüsü"]
    
    display_text = f"**Tahmin Edilen Sonuç:** {result_label} \n\n**Güven Skoru:** {confidence_percentage}"
    
    if result_label == "Sağlıklı":
        st.success(display_text)
    elif result_label in yellow_alerts:
        st.warning(display_text)
    elif result_label in red_alerts:
        st.error(display_text)

    if result_label != "Sağlıklı":
        db_data = get_disease_info(result_label)
        
        if db_data:
            neden_metni, onlem_metni = db_data 
            st.markdown("---")
            st.subheader("Hastalık Hakkında Bilgiler", anchor=False)
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Neden Ortaya Çıkar?", expanded=True):
                    st.write(neden_metni)
            with col2:
                with st.expander("Nasıl Engellenir?", expanded=True):
                    st.write(onlem_metni)
        else:
            st.info("Bu hastalık için veritabanında detaylı bilgi bulunmuyor.")
    else:

        st.info("Bitkiniz sağlıklı görünüyor! Düzenli bakıma devam ederek bu durumu koruyabilirsiniz.")