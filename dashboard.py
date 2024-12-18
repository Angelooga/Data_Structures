# from text import TextContent
# from code import CodeContent
import streamlit as st
import subprocess
import requests
import os

# JDoodle API settings
API_URL = "https://api.jdoodle.com/v1/execute"
CLIENT_ID = st.secrets["client_id"]
CLIENT_SECRET = st.secrets["client_secret"]

def compile_c_code(api_url, client_id, client_secret, code):
    payload = {
        "script": code,
        "language": "c",
        "versionIndex": "0",
        "clientId": client_id,
        "clientSecret": client_secret
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

class CreateDashboard:
    def __init__(self, topic):
        self.topic = topic
        self.content = {
            "intro": {
                "intro": {
                    "text": "intro.txt",
                    "images": {
                        "arreglo_c.png": None,
                        "arreglos.png": "Ejemplo de un arreglo",
                        "lista-enlazada.jpg": "Ejemplo de lista enlazada",
                        "grafos.png": "Ejemplo de un grafo",
                        "pilas_colas.png": "Ejemplo de pilas y colas",
                        "arbol.png": "Ejemplo de un árbol"
                    },
                    "code": None
                },
            },
            "static_structures": {
                "introduction": {
                    "text": "introduction.txt",
                    "images": {
                        "static_ds.jpg": "Arreglo como ejemplo de una estructura estática",
                    }
                },
                "arrays": {
                    "text": "arrays.txt",
                    "images": {
                        "arreglos.png": "Ejemplo de un arreglo",
                        "2d_arreglos.jpg": "Ejemplo de un arreglo bidimensional"
                    }
                },
                "dynamic_memory": {
                    "text": "dynamic_memory.txt",
                    "images": None
                },
                "queues_using_arrays": {
                    "text": "queues.txt",
                    "images": {
                        "queue_life.jpg": "Cola en la vida real",
                        "cola_estructura.png": "Estructura de una cola"
                    }
                },
                "stacks_using_arrays": {
                    "text": "stacks.txt",
                    "images": {
                        "stack.png": "Ejemplo de una pila",
                        "platos.jpg": "Ejemplo de una pila en la vida real"
                    }
                }
            },
            "dynamic_structures": {
                "introduction":{
                    "text": "introduction.txt",
                    "images": None
                },
                "linked_lists": {
                    "text": "linked_lists.txt",
                    "images": {
                        "queue.png": None
                    }
                },
                "double_lists": {
                    "text": "double_lists.txt",
                    "images": {
                        "double_structure.png": None,
                    }
                },
                "circular_lists": {
                    "text": "circular_lists.txt",
                    "images": {
                        "circular_representation.png": None,
                        "simple_circular.png": None
                    }
                },
                "binary_tree": {
                    "text": "binary_tree.txt",
                    "images": {
                        "introduction_tree.png": None,
                        "tree_creation.png": None,
                        "tree_elimination.png": None,
                        "tree_insertion.png": None,
                        "tree_parts.png": None
                    }
                }
            },
            "sorting_algorithms": {
                "introduction":{
                    "text": "introduction.txt",
                    "images": None
                },
                "bubble_sort": {
                    "text": "bubble_sort.txt",
                    "images": {
                        "BubbleSort.png": "Ilustración del algoritmo Bubble Sort"
                    }
                },
                "insertion_sort": {
                    "text": "insertion_sort.txt",
                    "images": {
                        "queue_life.jpg": "Cola en la vida real",
                        "InsertionSort.png": "Ilustración del Insertion Sort"
                    }
                },
                "merge_sort": {
                    "text": "merge_sort.txt",
                    "images": {
                        "MergeSort.png": "Ilustración del Merge Sort"
                    }
                },
                "quick_sort": {
                    "text": "quick_sort.txt",
                    "images": {
                        "Quicksort.png": "Ilustración del Quick Sort"
                    }
                }
            },
            "search_algorithms": {
                    "search_algorithms": {
                    "text": "SearchAlgorithm.txt",
                    "images": {
                        "bst_1.png": None,
                        "bst_2.png": None,
                        "busqueda_binaria.png": None,
                        "busqueda_secuencial.png": None,
                        "complejidad_busqueda_binaria.png": None
                    }
                }
            }
        }
        self.tabs = {
            "intro": ["Introducción"],
            "static_structures": ["Introducción", "Arreglos", "Asignación de Memoria Dinámica", "Colas", "Stacks"],
            "dynamic_structures": ["Introducción", "Listas Ligadas", "Listas Doblemente Ligadas", "Listas Circulares",
                                   "Árbol Binario"],
            "sorting_algorithms": ["Introducción", "Bubble Sort", "Insertion Sort","Merge Sort", "Quick Sort"],
            "search_algorithms": ["Algoritmos de Búsqueda"]
        }
        self.image_formats = [".jpg", ".png"]
        self.language_code = "c"

    def display_text(self, data, key):
        """
        This method does something...
        :return:
        """

        name = data["text"]
        path = f"{self.topic}/{key}/text/{name}"
        text_content = open(path, "r", encoding='utf-8').read().split("\n\n")

        for text in text_content:

            if text[-4:] in self.image_formats:
                image_path = f"{self.topic}/{key}/images/{text}"
                left_co, cent_co, last_co = st.columns([0.1, 0.8, 0.1])
                with cent_co:
                    st.image(image_path, data["images"][text])
                continue

            elif text[:4] == "code":
                self.display_code(key, text)
                continue

            # st.markdown(fr"{text}", unsafe_allow_html=True)
            st.markdown(fr"{text}", unsafe_allow_html=True)

    def display_code(self, key, name):
        """
        This method does something...
        :param data:
        :return:
        """
        path = f"{self.topic}/{key}/code/{name}"
        code_content = open(path, "r").read()

        st.markdown("##### Código de Ejemplo")

        # Display the "intro" code
        selected_code = code_content
        st.code(selected_code, language=self.language_code)

        # Button to run the code
        if st.button("Run Code", key=name):
            if code_content.strip():
                st.info("Compiling and running the code...")
                result = compile_c_code(API_URL, CLIENT_ID, CLIENT_SECRET, code_content)
                if result["error"]:
                    st.error(result["error"])
                else:
                    st.text(result["output"])

    def display_dashboard(self):
        """
        This method does something...
        :return:
        """

        data = self.content[self.topic]
        keys = list(data.keys())
        tabs = self.tabs[self.topic]

        shown_tabs = st.tabs(tabs)

        for i in range(len(tabs)):
            with shown_tabs[i]:

                self.display_text(data[keys[i]], keys[i])
