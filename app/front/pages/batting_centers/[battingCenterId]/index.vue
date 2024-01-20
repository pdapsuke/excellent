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

interface UpdateAttaNakattaResponse{
  id: number
  atta_count: number
  nakatta_count: number
  atta: string
  nakatta: string
}

// パスパラメータ(itemId)を取得
const { battingCenterId } = useRoute().params
const batterBox = ref<string>()
const username = useAuth().getUsername<string>()
const alert = ref<any>(null)

let machineInformations = ref<MachineInformation[]>()
let selectedBallSpeeds = ref<number[]>([])
let selectedBreakingBalls = ref<number[]>([])
let updateAttaNakattaResponse = ref<UpdateAttaNakattaResponse>()
let updateAttaNakattaError = ref<any>()

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

// あった！フラグに応じてあった！を登録/解除
async function atta(machineInformation: MachineInformation) {
  // あった！フラグが"yes"の場合、あった！ユーザーの追加
  if (machineInformation.atta == "yes") {
    ({ data: updateAttaNakattaResponse, error: updateAttaNakattaError } =  await useMachineInformationApi().addAttaUser(battingCenterId, machineInformation.id))

  // 行った！フラグが"no"の場合、行った！ユーザーの削除
  } else if (machineInformation.atta == "no") {
    ({ data: updateAttaNakattaResponse, error: updateAttaNakattaError } =  await useMachineInformationApi().removeAttaUser(battingCenterId, machineInformation.id))

  // 行った！フラグが"yes", "no"以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!updateAttaNakattaResponse.value || updateAttaNakattaError.value) {
    alert.value.error(updateAttaNakattaError.value)
    console.error(updateAttaNakattaError.value)
    return
  }

  // あった！なかった！フラグ数を更新
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].atta = updateAttaNakattaResponse.value.atta
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].atta_count = updateAttaNakattaResponse.value.atta_count
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].nakatta = updateAttaNakattaResponse.value.nakatta
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].nakatta_count = updateAttaNakattaResponse.value.nakatta_count
}

// なかった！フラグに応じてなかった！を登録/解除
async function nakatta(machineInformation: MachineInformation) {
  // なかった！フラグが"yes"の場合、なかった！ユーザーの追加
  if (machineInformation.nakatta == "yes") {
    ({ data: updateAttaNakattaResponse, error: updateAttaNakattaError } =  await useMachineInformationApi().addNakattaUser(battingCenterId, machineInformation.id))

  // 行った！フラグが"no"の場合、行った！ユーザーの削除
  } else if (machineInformation.atta == "no") {
    ({ data: updateAttaNakattaResponse, error: updateAttaNakattaError } =  await useMachineInformationApi().removeNakattaUser(battingCenterId, machineInformation.id))

  // 行った！フラグが"yes", "no"以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!updateAttaNakattaResponse.value || updateAttaNakattaError.value) {
    alert.value.error(updateAttaNakattaError.value)
    console.error(updateAttaNakattaError.value)
    return
  }

  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].atta = updateAttaNakattaResponse.value.atta
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].atta_count = updateAttaNakattaResponse.value.atta_count
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].nakatta = updateAttaNakattaResponse.value.nakatta
  machineInformations.value.filter((x) => x.id == machineInformation.id)[0].nakatta_count = updateAttaNakattaResponse.value.nakatta_count
}

</script>
