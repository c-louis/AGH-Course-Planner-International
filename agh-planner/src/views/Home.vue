<template>
  <main class="semesters">
    <section class="winter">
      <aside>
        <h3>Winter Semester : {{ winterHours()[4] }} Hours <a @click="hideShowWinter()"><small>Hide / Show</small></a></h3>
        <h4>
          {{ winterCredits() }}/30 credits 
          | {{ winterHours()[0] }} Lectures hour(s) 
          | {{ winterHours()[1] }} Laboratory hour(s) 
          | {{ winterHours()[2] }} Auditorium hour(s)
          | {{ winterHours()[3] }} Project hour(s)
        </h4>
        <table v-if="hideShowW">
          <thead>
            <tr>
              <th>SL</th>
              <th>Name</th>
              <th>Lecture</th>
              <th>Laboratory</th>
              <th>Auditorium</th>
              <th>Project</th>
              <th>Credits</th>
              <th>Examination</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in winterCourses" v-bind:key="course[0]" :class="{selected: course[8] != 'false'}">
              <td><input type="checkbox" @change="selectCourse(course)" :checked="course[8] == 'true'"></td>
              <td @click="showModal(course[0])">{{ course[1] }}</td>
              <td>{{ course[2] }} hrs</td>
              <td>{{ course[3] }} hrs</td>
              <td>{{ course[4] }} hrs</td>
              <td>{{ course[5] }} hrs</td>
              <td>{{ course[6] }}</td>
              <td>{{ course[7] }}</td>
            </tr>
          </tbody>
        </table>
      </aside>
    </section>
    <section class="summer">
      <aside>
        <h3>Summer Semester : {{ summerHours()[4] }} Hours <a @click="hideShowSummer()"><small>Hide / Show</small></a></h3>
        <h4>
          {{ summerCredits() }}/30 credits 
          | {{ summerHours()[0] }} Lectures hour(s) 
          | {{ summerHours()[1] }} Laboratory hour(s) 
          | {{ summerHours()[2] }} Auditorium hour(s)
          | {{ summerHours()[3] }} Project hour(s)
        </h4>
        <table v-if="hideShowS">
          <thead>
            <tr>
              <th>SL</th>
              <th>Name</th>
              <th>Lecture</th>
              <th>Laboratory</th>
              <th>Auditorium</th>
              <th>Project</th>
              <th>Credits</th>
              <th>Examination</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in summerCourses" v-bind:key="course[0]" :class="{selected: course[8] != 'false'}">
              <td><input type="checkbox" @change="selectCourse(course)" :checked="course[8] == 'true'"></td>
              <td @click="showModal(course[0])">{{ course[1] }}</td>
              <td>{{ course[2] }} hrs</td>
              <td>{{ course[3] }} hrs</td>
              <td>{{ course[4] }} hrs</td>
              <td>{{ course[5] }} hrs</td>
              <td>{{ course[6] }}</td>
              <td>{{ course[7] }}</td>
            </tr>
          </tbody>
        </table>
      </aside>
    </section>
  </main>
</template>

<script>

//const csv = require('csv-parser')
import winterCourses from 'raw-loader!../assets/winter_courses.csv'
import summerCourses from 'raw-loader!../assets/summer_courses.csv'
import * as CSV from 'csv-string';
const axios = require('axios').default;

export default {
  name: 'Home',
  data() {
    return {
      winterCourses: [],
      summerCourses: [],
      modalsContents: [],
      hideShowW: true,
      hideShowS: true
    }
  },
  mounted() {
    this.winterCourses = CSV.parse(winterCourses);
    this.summerCourses = CSV.parse(summerCourses);

    // Set selected course or not from localStorage
    for (let course of this.winterCourses) {
      let selected = localStorage.getItem(course[0])
      if (selected == null) {
        selected = false
        localStorage.setItem(course[0], false)
      }
      course.push(selected)
    }
    for (let course of this.summerCourses) {
      let selected = localStorage.getItem(course[0])
      if (selected == null) {
        selected = false
        localStorage.setItem(course[0], false)
      }
      course.push(selected)
    }
    for (let course of this.winterCourses) {
      this.getModalContent(course[0]).then((response) => {
        this.modalsContents[course[0]] = response;
      })
    }
    for (let course of this.summerCourses) {
      this.getModalContent(course[0]).then((response) => {
        this.modalsContents[course[0]] = response;
      })
    }
  },
  methods: {
    selectCourse(course) {
      var toChange = this.winterCourses.find(element => element[0] == course[0])
      if (toChange == undefined) {
        toChange = this.summerCourses.find(element => element[0] == course[0])
      }
      toChange[8] = toChange[8] == 'true' ? 'false' : 'true';
      localStorage.setItem(toChange[0], toChange[8]);
      this.$forceUpdate()
    },
    winterCredits() {
      var creditCount = 0;
      for (var course of this.winterCourses) {
        if (course[8] == 'true') {
          creditCount += parseInt(course[6])
        }
      }
      return creditCount;
    },
    summerCredits() {
      var creditCount = 0;
      for (var course of this.summerCourses) {
        if (course[8] == 'true') {
          creditCount += parseInt(course[6])
        }
      }
      return creditCount;
    },
    winterHours() {
      var hours = [0, 0, 0, 0, 0];
      for (var course of this.winterCourses) {
        if (course[8] == 'true') {
          hours[0] += parseInt(course[2])
          hours[1] += parseInt(course[3])
          hours[2] += parseInt(course[4])
          hours[3] += parseInt(course[5])
        }
      }
      hours[4] = hours.reduce((partialSum, a) => partialSum + a, 0);
      return hours;
    },
    summerHours() {
      var hours = [0, 0, 0, 0, 0];
      for (var course of this.summerCourses) {
        if (course[8] == 'true') {
          hours[0] += parseInt(course[2])
          hours[1] += parseInt(course[3])
          hours[2] += parseInt(course[4])
          hours[3] += parseInt(course[5])
        }
      }
      hours[4] = hours.reduce((partialSum, a) => partialSum + a, 0);
      return hours;
    },
    async getModalContent(id) {
      var response = await axios.get('https://agh.cl-dev.ovh/api.php?id=' + id);
      if (response.status != 200) {
        return '';
      }
      console.log("Got : " + id)
      return response.data.html;
    },
    showModal(id) {
      var el = document.createElement('html');
      el.innerHTML = this.modalsContents[id];
      var body = el.getElementsByTagName('body')[0]
      var syllabus = body.childNodes[7]
      this.$modal.show(
        {
          template: syllabus.outerHTML,
        },
        { },
        { width: '900px', height: '1000px'},
      );
    },
    hideShowWinter() {
      this.hideShowW = !this.hideShowW
    },
    hideShowSummer() {
      this.hideShowS = !this.hideShowS
    }
  },
}
</script>
