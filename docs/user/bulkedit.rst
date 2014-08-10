****************************
Editing multiple assignments
****************************
To ease handling of editing multiple assignments at the same time
Trix provides a YAML based format which fully supports the need for bulk managment

Multiple editing will opt in as an action when you check several assignments in the
assignment view as shown in the image below.

.. image:: images/bulkedit.png


Format
======
Read up on YAML: `yaml_wikipedia`_ 

Each assignment are associated with the following fields:

id : 
    Internal unique identifier.
title : 
    The title of the assignment.
tags : 
    Tags to classify the assignments.
text : 
    The assignment text to describe the problem to solve.
solution : 
    The solution to the problem of the assignment.

The fields are rendered within the YAML format as listed below.

.. code-block:: none

    id: 4
    title: '<title>'
    tags: [tag1, tag2, tag3, ...]
    text: |-
        <assignment text>
    solution: |-
        ``` java
            class Solution {

            }
        ```


.. _yaml_wikipedia: http://en.wikipedia.org/wiki/YAML

Example
=======

.. code-block:: none

    id: 4
    title: 'Utskrift og sum av oddetalls-array:'
    tags: [inf1000, vår2014, oblig1]
    text: |-
      Skriv et program som inneholder en heltalls-array med følgende elementer: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19.  Programmet skal inneholde en løkke som skriver ut indeksen og verdien for alle elementene i arrayen.
    solution: |-
      ``` java
      class Oddetall {
        public static void main(String[] args) {
          int[] oddetall = { 1, 3, 5, 7, 9, 11, 13, 15, 17, 19 };
          for (int i = 0; i < oddetall.length; i++) {
            System.out.println("oddetall[" + i + "] = " + oddetall[i]);
          }
        }
      }
      ```
    ---
    id: 1
    title: Hello World
    tags: [inf1000, vår2014, uke1, oblig1]
    text: |-
      Print hello world in the terminal.
    solution: |-
      ``` java
      public class HelloWorld {
          public static void main(String [] args) {
              System.out.println("Hello World!");
          }
      }
      ```