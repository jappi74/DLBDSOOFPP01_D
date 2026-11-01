import streamlit as st
from datetime import date
import plotly.graph_objects as go
from controller import DashboardController

class DashboardView:
    def __init__(self, controller: DashboardController):
        self._controller = controller

    def render(self):
        st.set_page_config(page_title="Studien-Dashboard", layout="wide")
        student = self._controller.student
        
        st.title(f"{student.studiengang.name}")
        st.write(f"Willkommen im Dashboard von **{student.name}** .")

        daten = self._controller.berechne_zeitliche_zielerreichung()
        schnitt_ist, schnitt_ziel = self._controller.berechne_notendurchschnitt()

        # Kacheln für die Metriken
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Erreichte CPs", value=f"{daten['erreichte_cps']} / {daten['gesamt_cps']}")
            st.metric(label="Durchschnittliche Zeit pro CP", value=f"{daten['ist_tage_pro_cp']} Tage / {daten['soll_tage_pro_cp']} Tage")
        with col2:
            st.metric(label="Abgelegte Prüfleistungen", value=f"{daten['bestanden_anzahl']} / {daten['gesamt_anzahl']}")
            st.metric(label="Notendurchschnitt", value=f"{schnitt_ist} / {schnitt_ziel}")

        st.divider()
        
        # Zeitstrahl
        st.subheader("Zeitlicher Studienverlauf & Zielerreichung (Regelstudienzeit)")
        
        diff = daten["cp_differenz"]
        is_ahead = diff >= 0
        status_text = f"Vorsprung von {diff} CPs" if is_ahead else f"Rückstand von {abs(diff)} CPs"
        status_farbe = "green" if is_ahead else "red"
        
        st.markdown(f"Status bezüglich Regelstudienzeit: **:{status_farbe}[{status_text}]** (Ist heute: **{daten['erreichte_cps']} CPs** | Soll heute laut Plan: **{daten['soll_cps_heute']} CPs**)")

        gesamttage = (daten["end_datum"] - daten["start_datum"]).days
        heute_tage = (date.today() - daten["start_datum"]).days
        
        # Berechnung des Tages, zu dem man die aktuellen CPs erreicht haben sollte mit Blick auf Zielerreichung
        tag_fuer_ist_cps = int(daten['erreichte_cps'] * daten['soll_tage_pro_cp'])
        
        fig = go.Figure()

        # Studienbalken
        fig.add_trace(go.Bar(
            x=[gesamttage],
            y=["Studienverlauf"],
            orientation='h',
            marker=dict(color='#e0e0e0'),
            hoverinfo='none',
            showlegend=False
        ))

        # Markierung Soll-Stand des aktuellen Tages in Bezug auf Zeitziel und erreichte CPs
        fig.add_vline(
            x=heute_tage,
            line_width=3, line_dash="dash", line_color="orange",
            annotation_text=f"Heutiger Tag / Soll ({daten['soll_cps_heute']} CPs erwartet)", annotation_position="top left"
        )

        # Markierung Ist-Stand des aktuellen Tages in Bezug auf Zeitziel und erreichte CPs
        fig.add_vline(
            x=tag_fuer_ist_cps,
            line_width=3, line_color="green" if is_ahead else "red",
            annotation_text=f"Normaler Tag für {daten['erreichte_cps']} CPs (Tag {tag_fuer_ist_cps})", annotation_position="top right"
        )

        fig.update_layout(
            xaxis_title="Tage im Studienverlauf",
            yaxis_showgrid=False,
            height=200,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Tabellarische Modulübersicht
        st.divider()
        st.subheader("Modulübersicht und Leistungsstand")
        
        modul_liste = []
        for modul in student.studiengang.module:
            pl = modul.pruefungsleistung
            modul_liste.append({
                "Modul": modul.bezeichnung,
                "CP": modul.credit_points,
                "Form": pl.pruefungsform.value,
                "Note": pl.note if pl.note is not None else "Offen",
                "Status": "Bestanden" if pl.ist_bestanden else "In Bearbeitung"
            })
        
        st.table(modul_liste)