<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="text-h4">{{ detail.name }}</div>
      <v-select
        v-model="selectedBallSpeeds"
        variant="outlined"
        label="球速"
        :items="ballSpeeds"
        item-title="speed"
        item-value="id"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="selectedBreakingBalls"
        variant="outlined"
        label="球種"
        :items="breakingBalls"
        item-title="name"
        item-value="id"
        clearable
        multiple
        dense
      ></v-select>
      <v-select
        v-model="batterBox"
        variant="outlined"
        label="打席"
        :items="[{id: 1, value: '左'}, {id: 2, value: '右'}, {id: 3, value: '両'}]"
        item-title="value"
        item-value="value"
        clearable
        dense
      ></v-select>
      <div class="d-flex justify-end">
        <v-btn color="secondary" class="mr-4" type="submit" @click.prevent="post">投稿</v-btn>
      </div>
    </div>
    <div class="mb-3">
      <v-table>
        <thead>
          <tr>
            <th class="text-left">球速 km/h</th>
            <th class="text-left">球種</th>
            <th class="text-left">打席</th>
            <th class="text-left">更新日</th>
            <th class="text-left">あった！数</th>
            <th class="text-left">あった！ボタン</th>
            <th class="text-left">なかった！数</th>
            <th class="text-left">なかった！ボタン</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="machine_information in machineInformations"
            :key="machine_information.id">
            <td>{{ machine_information.ball_speeds.map((x) => x.speed).join(", ") }}</td>
            <td>{{ machine_information.breaking_balls.map((x) => x.name).join(", ") }}</td>
            <td>{{ machine_information.batter_box }}</td>
            <td>{{ dateFormat(machine_information.updated) }}</td>
            <td>{{ machine_information.atta_count }}</td>
            <td>
              <v-switch
                v-model="machine_information.atta"
                color="primary"
                hide-details
                true-value="yes"
                false-value="no"
                :label="`${machine_information.atta}`"
                @change="atta(machine_information)"
              ></v-switch>
            </td>
            <td>{{ machine_information.nakatta_count }}</td>
            <td>
              <v-switch
                v-model="machine_information.nakatta"
                color="primary"
                hide-details
                true-value="yes"
                false-value="no"
                :label="`${machine_information.nakatta}`"
                @change="nakatta(machine_information)"
              ></v-switch>
            </td>
          </tr>
        </tbody>
      </v-table>      
    </div>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

interface BreakingBall {
  id: number
  name: string
}

interface BallSpeed {
  id: number
  speed: number
}

interface MachineInformation{
  id: number
  user_id: number
  breaking_balls: BreakingBall[]
  ball_speeds: BallSpeed[]
  atta_count: number
  atta: string
  nakatta_count: number
  nakatta: string
  updated: string
}

// パスパラメータ(itemId)を取得
const { battingCenterId } = useRoute().params
const batterBox = ref<string>()
const username = useAuth().getUsername<string>()
const alert = ref<any>(null)

let machineInformations = ref<MachineInformation>()
let selectedBallSpeeds = ref<number[]>([])
let selectedBreakingBalls = ref<number[]>([])

const { data: detail, error: detailError } = await useBattingCenterApi().getDetail(battingCenterId)

// バッティングセンター詳細の取に失敗した場合、アラートとログを出力
if (!detail.value || detailError.value) {
  alert.value.error(detailError.value)
  console.error(detailError.value)
} else {
  machineInformations.value = detail.value.machine_informations
}


const { data: ballSpeeds, error: ballSpeedsError } = await useMachineInformationApi().getBallSpeeds()

if (!ballSpeeds.value || ballSpeedsError.value) {
  alert.value.error(ballSpeedsError.value)
  console.error(ballSpeedsError.value)
}

const { data: breakingBalls, error: breakingBallsError } = await useMachineInformationApi().getBreakingBalls()

// 球種一覧の取得に失敗した場合、アラートとログを出力
if (!breakingBalls.value || breakingBallsError.value) {
  alert.value.error(breakingBallsError.value)
  console.error(breakingBallsError.value)
}

function dateFormat(datetime: string) {
  const updated_date = new Date(datetime) 
  const year = updated_date.getFullYear()
  const month = updated_date.getMonth() + 1
  const day = updated_date.getDate()
  const hour = updated_date.getHours()
  const minute = updated_date.getMinutes()

  return `${year}/${month}/${day} ${hour}:${minute}`
}

async function post() {
  const { data: postResponse, error: postError } = await useMachineInformationApi().postMachineInformation(
    battingCenterId,
    {
      ballspeed_ids: selectedBallSpeeds.value,
      breaking_ball_ids: selectedBreakingBalls.value,
      batter_box: batterBox.value,
    }
  )

  if (!postResponse.value || postError.value) {
    alert.value.error(postError.value)
    console.error(postError.value)
    return
  }

  const { data: machineInformationsFromAPI, error: getMachineInformationsError } = await useMachineInformationApi().getMachineInformation(battingCenterId)

  if (!machineInformationsFromAPI.value || getMachineInformationsError.value) {
    alert.value.error(getMachineInformationsError.value)
    console.error(getMachineInformationsError.value)
    return
  }

  machineInformations.value = machineInformationsFromAPI.value
  selectedBallSpeeds.value = undefined
  selectedBreakingBalls.value = undefined
  batterBox.value = undefined
}

// あった！を登録/解除
async function atta(machine_information: any) {
  const { data: atta_response, pending:atta_pending, error: atta_error, refresh: atta_refresh } =  await useUserApi().updateAttaNakatta({
    username: username,
    machine_id: machine_information.id,
    atta_nakatta: "atta",
    add_atta_nakatta: machine_information.atta
  })
  refresh()
}

// なかった！を登録/解除
async function nakatta(machine_information: any) {
  const { data: nakatta_response, pending: nakatta_pending, error: nakatta_error, refresh: nakatta_refresh } =  await useUserApi().updateAttaNakatta({
    username: username,
    machine_id: machine_information.id,
    atta_nakatta: "nakatta",
    add_atta_nakatta: machine_information.nakatta
  })
  refresh()
}

</script>
