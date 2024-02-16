<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="text-h4">{{ detail.name }}</div>
    </div>
    <div class="mb-3">
      <Carousel :autoplay="5000" :wrapAround="true">
        <Slide v-for="image in images" :key="image">
          <v-img
            :src="image"
            contain
            max-height="400"
            max-width="800"
          ></v-img>
        </Slide>
        <template #addons>
          <Pagination />
        </template>
      </Carousel>
    </div>
    <div class="mb-3">
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
            <th class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="machine_information in machineInformations"
            :key="machine_information.id">
            <td>{{ machine_information.ball_speeds.map((x) => x.speed).join(", ") }}</td>
            <td>{{ machine_information.breaking_balls.map((x) => x.name).join(", ") }}</td>
            <td>{{ machine_information.batter_box }}</td>
            <td>{{ useUtil().formatDate(machine_information.updated) }}</td>
            <td>{{ machine_information.atta_count }}</td>
            <td>
              <AttaButton
                :atta="machine_information.atta"
                @click="atta(machine_information)"
              >
              </AttaButton>
            </td>
            <td>{{ machine_information.nakatta_count }}</td>
            <td>
              <NakattaButton
                :nakatta="machine_information.nakatta"
                @click="nakatta(machine_information)"
              >
              </NakattaButton>
            </td>
            <td>
              <div class="d-flex">
                <div>
                  <v-btn icon flat v-if="machine_information.is_owner==true"
                    @click="editDialog.open({
                      ball_speeds: ballSpeeds,
                      breaking_balls: breakingBalls,
                      batter_box: machine_information.batter_box,
                      selected_ball_speeds: useUtil().createSelectedBallSpeedsList(machine_information),
                      selected_breaking_balls: useUtil().createSelectedBreakingBallsList(machine_information),
                      machineId: machine_information.id})"
                      ><v-icon color="warning" :icon="mdiNoteEditOutline"></v-icon>
                  </v-btn>
                </div>
                <div>
                  <v-btn icon flat v-if="machine_information.is_owner==true" @click="confirmDeletion.open({machineId: machine_information.id})">
                    <v-icon color="error" :icon="mdiDeleteForeverOutline"></v-icon>
                  </v-btn>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </v-table>      
    </div>
    <!-- 削除確認ダイアログ -->
    <ConfirmDialog
      title="マシン情報の削除"
      message="本当に削除しますか"
      confirmBtn="削除"
      cancelBtn="キャンセル"
      colorCancel="primary"
      colorConfirm="error"
      ref="confirmDeletion"
      @confirm="deleteMachineInformation">
    </ConfirmDialog>
    <!-- 編集確認ダイアログ -->
    <EditDialog
      title="マシン情報の編集"
      confirmBtn="OK"
      cancelBtn="キャンセル"
      colorCancel="primary"
      colorConfirm="error"
      ref="editDialog"
      @confirm="editMachineInformation">
    </EditDialog>
  </div>
</template>

<script setup lang="ts">
import { mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

// ミドルウェアによるログインチェック
definePageMeta({ middleware: ["auth"] })

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
  is_owner: boolean
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
const username = useAuth().getUsername<string>()
const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)
const editDialog = ref<any>(null)
const images = ref<string[]>(null)

let batterBox = ref<string>()
let machineInformations = ref<MachineInformation[]>()
let selectedBallSpeeds = ref<number[]>([])
let selectedBreakingBalls = ref<number[]>([])
let attaNakattaUpdateResponse = ref<UpdateAttaNakattaResponse>()
let attaNakattaUpdateError = ref<any>()

const { data: detail, error: detailError } = await useBattingCenterApi().getDetail(battingCenterId)

// バッティングセンター詳細の取得に失敗した場合、アラートとログを出力
if (!detail.value || detailError.value) {
  alert.value.error(detailError.value)
  console.error(detailError.value)
} else {
  machineInformations.value = detail.value.machine_informations
  images.value = detail.value.photos
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

// 投稿、更新、削除後、マシン情報一覧を更新する処理
async function updateMachineInformationList() {
  const { data: machineInformationsFromAPI, error: getMachineInformationsError, refresh: refreshMachineInformations } = await useMachineInformationApi().getMachineInformation(battingCenterId)

  if (!machineInformationsFromAPI.value || getMachineInformationsError.value) {
    alert.value.error(getMachineInformationsError.value)
    console.error(getMachineInformationsError.value)
    return
  }

  machineInformations.value = machineInformationsFromAPI.value
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

  await updateMachineInformationList()

  // 選択したチェックボックスは空欄にする
  selectedBallSpeeds.value = undefined
  selectedBreakingBalls.value = undefined
  batterBox.value = undefined
}

// あった！フラグに応じてあった！を登録/解除
async function atta(machineInformation: MachineInformation) {
  // あった！フラグが"no"の場合、あった！ユーザーの追加
  if (machineInformation.atta == "no") {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().addAttaUser(battingCenterId, machineInformation.id))

  // あった！フラグが"yes"の場合、あった！ユーザーの削除
  } else if (machineInformation.atta == "yes") {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().removeAttaUser(battingCenterId, machineInformation.id))

  // あった！フラグが"yes", "no"以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!attaNakattaUpdateResponse.value || attaNakattaUpdateError.value) {
    alert.value.error(attaNakattaUpdateError.value)
    console.error(attaNakattaUpdateError.value)
    return
  }

  useUtil().updateAttaNakattaForMachineInformation(machineInformations.value, machineInformation, attaNakattaUpdateResponse.value)
}

// なかった！フラグに応じてなかった！を登録/解除
async function nakatta(machineInformation: MachineInformation) {
  // なかった！フラグが"no"の場合、なかった！ユーザーの追加
  if (machineInformation.nakatta == "no") {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().addNakattaUser(battingCenterId, machineInformation.id))

  // なかった！フラグが"yes"の場合、なかった！ユーザーの削除
  } else if (machineInformation.nakatta == "yes") {
    ({ data: attaNakattaUpdateResponse, error: attaNakattaUpdateError } =  await useMachineInformationApi().removeNakattaUser(battingCenterId, machineInformation.id))

  // なかった！フラグが"yes", "no"以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }

  if (!attaNakattaUpdateResponse.value || attaNakattaUpdateError.value) {
    alert.value.error(attaNakattaUpdateError.value)
    console.error(attaNakattaUpdateError.value)
    return
  }

  useUtil().updateAttaNakattaForMachineInformation(machineInformations.value, machineInformation, attaNakattaUpdateResponse.value)
}

async function deleteMachineInformation(confirm: boolean, params: {machineId: number}) {
  // キャンセルされた場合は何もしない
  if (!confirm) { return }
  // マシン情報削除APIを呼び出す
  const { error } = await useMachineInformationApi().deleteMachineInformation(battingCenterId, params.machineId)

  if (error.value instanceof Error) {
    alert.value.error(error.value)
    console.error(error.value)
    return
  }
  // 成功: マシン情報一覧を更新
  await updateMachineInformationList()
}

async function editMachineInformation(
  confirm: boolean,
  parameters: any,
  selectedBatterBox: number[],
  selectedBallSpeeds: number[],
  selectedBreakingBalls: number[],
) {
  // キャンセルされた場合は何もしない
  if (!confirm) { return }
  // マシン情報更新APIを呼び出す
  const { data: updateMachineInformationResponse, error: updateMachineInformationError } = await useMachineInformationApi().updateMachineInformation(
    battingCenterId,
    parameters.machineId,
    {
      ballspeed_ids: selectedBallSpeeds,
      breaking_ball_ids: selectedBreakingBalls,
      batter_box: selectedBatterBox,
    })

  if (updateMachineInformationError.value instanceof Error) {
    alert.value.error(updateMachineInformationError.value)
    console.error(updateMachineInformationError.value)
    return
  }
  // 成功: マシン情報一覧を更新
  await updateMachineInformationList()
}
</script>
