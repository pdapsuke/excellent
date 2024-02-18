<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="d-flex align-center mb-2">
        <div class="text-h4 mr-13">{{ detail.name }}</div>
        <div class="text-h4 font-italic mr-3">{{ detail.itta_count }}</div>
        <div class="me-auto"><IttaButton :itta="detail.itta" @click="itta(detail)"></IttaButton></div>
        <div class="mr-5"><NuxtLink :to="`/`">検索画面に戻る</NuxtLink></div>
      </div>
      <div class="text-h7">{{ detail.formatted_address }}</div>
    </div>
    <v-row class="mb-5 d-flex align-center">
      <v-col cols="12" lg="6" sm="6">
        <div>
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
      </v-col>
      <v-col cols="12" lg="6" sm="6">
        <div>
          <div>
            <v-list lines="one">
              <v-list-item
                v-for="(item, i) in checkListsForPost"
                :key="i">
                <template v-slot:prepend>
                  <v-icon color="primary" :icon="mdiCheck"></v-icon>
                </template>
                <v-list-item-title v-text="checkListsForPost[i]"></v-list-item-title>
              </v-list-item>
            </v-list>
          </div>
          <div class="d-flex flex-row-reverse">
            <v-btn color="secondary" class="mr-4" type="submit" @click="createDialog.open({
              ball_speeds: ballSpeeds,
              breaking_balls: breakingBalls,
              })">新規投稿</v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
    <div class="mb-3">
      <v-table>
        <thead>
          <tr>
            <th class="text-left">球速 km/h</th>
            <th class="text-left">球種</th>
            <th class="text-left">打席</th>
            <th class="text-left">更新日</th>
            <th class="text-left"></th>
            <th class="text-left"></th>
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
            <td>
              <div class="d-flex justify-end align-center">
                <div>{{ machine_information.atta_count }}</div>
                <div>
                  <AttaButton
                    :atta="machine_information.atta"
                    @click="atta(machine_information)"
                  ></AttaButton>
                </div>
              </div>
            </td>
            <td>
              <div class="d-flex justify-start align-center">
                <div>{{ machine_information.nakatta_count }}</div>
                <div>
                  <NakattaButton
                    :nakatta="machine_information.nakatta"
                    @click="nakatta(machine_information)"
                  ></NakattaButton>
                </div>
              </div>
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
    <CreateDialog
      title="マシン情報の新規投稿"
      confirmBtn="投稿"
      cancelBtn="キャンセル"
      colorCancel="primary"
      colorConfirm="error"
      ref="createDialog"
      @confirm="createMachineInformation">
    </CreateDialog>
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
import { mdiCheck, mdiNoteEditOutline, mdiDeleteForeverOutline } from '@mdi/js'

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

interface IttaResponse {
    id: number
    itta_count: number
    itta: string
}

// パスパラメータ(itemId)を取得
const { battingCenterId } = useRoute().params
const username = useAuth().getUsername<string>()
const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)
const createDialog = ref<any>(null)
const editDialog = ref<any>(null)
const images = ref<string[]>(null)
const checkListsForPost = [
  "設置されているピッチングマシンの情報をシェアしよう！",
  "投稿はピッチングマシン1台毎",
  "あった！なかった！ボタンでマシンがあったか評価しよう！",
]

let batterBox = ref<string>()
let machineInformations = ref<MachineInformation[]>()
let selectedBallSpeeds = ref<number[]>([])
let selectedBreakingBalls = ref<number[]>([])
let attaNakattaUpdateResponse = ref<UpdateAttaNakattaResponse>()
let attaNakattaUpdateError = ref<any>()
let ittaResponse = ref<IttaResponse>()
let ittaError = ref<any>()

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

// 行った！フラグに応じて行った！を登録/解除
async function itta(detail: any) {
  // 行った！フラグが"yes"の場合、行った！ユーザーの追加
  if (detail.itta == "no") {
    ({ data: ittaResponse, error: ittaError } =  await useBattingCenterApi().addIttaUser(detail.id))
  // 行った！フラグが"no"の場合、行った！ユーザーの削除
  } else if (detail.itta == "yes") {
    ({data: ittaResponse, error: ittaError } =  await useBattingCenterApi().removeIttaUser(detail.id))
  // 行った！フラグが"yes", "no"以外の場合、エラー出力
  } else {
    alert.value.error("Bad Request")
    console.error("Bad Request")
    return
  }
  // レスポンスが正しく返ってこなかった場合、エラー出力
  if (!ittaResponse.value || ittaError.value) {
    alert.value.error(ittaError.value)
    console.error(ittaError.value)
    return
  }
  // 行った！フラグと行った数を更新
  detail.itta = ittaResponse.value.itta
  detail.itta_count = ittaResponse.value.itta_count
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

// マシン情報の新規作成
async function createMachineInformation(
  confirm: boolean,
  selectedBatterBox: number[],
  selectedBallSpeeds: number[],
  selectedBreakingBalls: number[],
) {
  // キャンセルされた場合は何もしない
  if (!confirm) { return }
  // マシン情報作成APIを呼び出す
  const { data: postResponse, error: postError } = await useMachineInformationApi().postMachineInformation(
    battingCenterId,
    {
      ballspeed_ids: selectedBallSpeeds,
      breaking_ball_ids: selectedBreakingBalls,
      batter_box: selectedBatterBox,
    }
  )

  if (!postResponse.value || postError.value) {
    alert.value.error(postError.value)
    console.error(postError.value)
    return
  }

  await updateMachineInformationList()
}

// マシン情報の編集
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
