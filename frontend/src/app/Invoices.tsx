import { PATH_DEFAULT, SERVER_LOCAL } from "@/utils/constants/server"
import { STATUS_PAYMENT, STATUS_PAYMENT_COLOR, STATUS_PAYMENTS } from "@/utils/constants/status"
import { BodyAddPaymentDetail, BodyRemoveProductToPayment } from "@/utils/domain/types/body.type"
import { PaymentContent, ProductContent, ResponseDefault, ResponseList, ResponseRemoveProductToPayment } from "@/utils/domain/types/responses.type"
import { useDeleteFetch, useGetFetch, usePostFetch } from "@/utils/hooks/fetch-data"
import { useGetLocalStorage } from "@/utils/hooks/local-storage"
import { format } from "@formkit/tempo"
import { Accordion, Badge, Button, Card, HR, Label, Modal, Select, TextInput } from "flowbite-react"
import { useEffect, useState } from "react"
import { HiBadgeCheck, HiClock, HiOutlineExclamationCircle, HiXCircle } from "react-icons/hi"
import { MdOutlineCancel } from "react-icons/md"
import { VscIssueDraft } from "react-icons/vsc"
import { toast } from "react-toastify"

interface Props {
    children?: React.ReactNode
}

export default function InvoicesPage(_props: Props) {
    const [invoices, setInvoices] = useState<PaymentContent[]>([])
    const [products, setProducts] = useState<ProductContent[]>([])
    const [nextPage, setNextPage] = useState<string | null | undefined>(null)
    const [openModalAddPayment, setOpenModalAddPayment] = useState(false);
    const [openModalAddProductToPayment, setOpenModalAddProductToPayment] = useState(false);
    const [paymentDetail, setPaymentDetail] = useState({ id: "", product: "" })

    const exec_data = async () => {
        const myToken = useGetLocalStorage('token')
        const newList = await useGetFetch<ResponseList<ProductContent>>(SERVER_LOCAL, { path: `${PATH_DEFAULT}/products/`, params: [{ name: 'page_size', value: '100' }], tokenAuth: useGetLocalStorage('token') ?? "" }) as ResponseList<ProductContent>
        const data = await useGetFetch<ResponseList<PaymentContent>>(SERVER_LOCAL, { path: `${PATH_DEFAULT}/payments/`, tokenAuth: myToken ?? "" }) as ResponseList<PaymentContent>
        if (newList.results) {
            setProducts(newList.results)
        }
        if (data.results) {
            setNextPage(data.next)
            setInvoices(data.results)
        }
    }
    useEffect(() => {
        
        exec_data()
    }, [])

    return (
        <>
            <Card className='w-full max-w-screen-2xl mt-10'>
                <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    Facturas o Pagos
                </h5>
                <div className="flex flex-col md:flex-row">
                    <Button color="primary" onClick={() => setOpenModalAddPayment(true)}>
                        Crear nueva factura
                    </Button>
                </div>
            </Card>
            <Modal show={openModalAddPayment} size="md" onClose={() => setOpenModalAddPayment(false)} popup>
                <Modal.Header />
                <Modal.Body>
                    <div className="text-center">
                        <HiOutlineExclamationCircle className="mx-auto mb-4 h-14 w-14 text-gray-400 dark:text-gray-200" />
                        <h3 className="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
                            ¿Estas seguro de crear una nueva factura?
                        </h3>
                        <div className="flex justify-center gap-4">
                            <Button color="primary" onClick={async () => {
                                const response = await usePostFetch(SERVER_LOCAL, { path: '/api/v1/payments/', tokenAuth: useGetLocalStorage('token') ?? "" })
                                toast(response.detail, { type: 'info' })
                                setOpenModalAddPayment(false)
                                await exec_data()
                            }}>
                                {"Si, Lo estoy"}
                            </Button>
                            <Button color="gray" onClick={() => setOpenModalAddPayment(false)}>
                                No, cancelar
                            </Button>
                        </div>
                    </div>
                </Modal.Body>
            </Modal>
            <Modal show={openModalAddProductToPayment} onClose={() => setOpenModalAddProductToPayment(false)}>
                <Modal.Header>Agregar producto</Modal.Header>
                <Modal.Body>
                    <div className="space-y-6">
                        <div className="max-w-md">
                            <div className="mb-2 block">
                                <Label htmlFor="product-select" value="Elija el producto" />
                            </div>
                            <Select id="product-select" defaultValue={"0"} onChange={(event) => {
                                setPaymentDetail((before) => ({ ...before, product: event.target.value }))
                            }} required>
                                <option className="font-medium" color="gray" value={"0"} >-- Elegir producto --</option>
                                {
                                    products.map(product => (
                                        <option key={product.id} value={product.id}>{product.name}</option>
                                    ))
                                }
                            </Select>
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button color="gray" onClick={() => setOpenModalAddProductToPayment(false)}>
                        Cancelar
                    </Button>
                    <Button color="primary" onClick={async () => {
                        const response = await usePostFetch<ResponseDefault, BodyAddPaymentDetail>(SERVER_LOCAL, {
                            path: `/api/v1/payments/${paymentDetail.id}/add_detail/`, data: {
                                product: paymentDetail.product
                            },
                            tokenAuth: useGetLocalStorage('token') ?? ""
                        }) as ResponseDefault
                        toast(response.detail ?? "Se ha agregado un nuevo producto.", { type: 'info' })
                        setOpenModalAddProductToPayment(false)
                        await exec_data()
                    }}>Agregar producto</Button>
                </Modal.Footer>
            </Modal>
            <Card className='w-full gap-2 max-w-screen-2xl'>
                {
                    invoices.map(item => (
                        <section className="w-full space-y-4" key={item.id}>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full" >
                                <div className="flex max-w-md flex-col gap-4">
                                    <Label htmlFor={`name-invoice-${item.id}`}>Monto Total</Label>
                                    <TextInput type="text" id={`total-invoice-${item.id}`} value={`$ ${Number(item.total_amount).toFixed(2)}`} placeholder={`$ ${Number(item.total_amount).toFixed(2)}`} disabled readOnly />
                                </div>

                                <div className="flex items-center justify-center h-auto flex-col gap-4">
                                    <Accordion collapseAll className="w-full">
                                        {
                                            item.payment_details.map(payment_detail => (
                                                <Accordion.Panel key={payment_detail.id}>
                                                    <Accordion.Title>{payment_detail.product.name}</Accordion.Title>
                                                    <Accordion.Content>
                                                        <div className="flex justify-end w-full">
                                                            <Button color="failure" className="gap-4" onClick={async () => {
                                                                const response = await usePostFetch<ResponseRemoveProductToPayment, BodyRemoveProductToPayment>(SERVER_LOCAL, {
                                                                    path: `/api/v1/payments/remove_detail/`,
                                                                    data: { payment_detail_id: payment_detail.id },
                                                                    tokenAuth: useGetLocalStorage('token') ?? ""
                                                                }) as ResponseRemoveProductToPayment
                                                                toast(response.detail, { type: 'info' })
                                                                window.location.reload()
                                                            }}>
                                                                <HiXCircle className="size-5" />
                                                                Eliminar
                                                            </Button>

                                                        </div>
                                                        <div className="flex flex-col gap-4">
                                                            <Label htmlFor={`serial-product-${payment_detail.id}`}>Serial producto</Label>
                                                            <TextInput type="text" id={`serial-product-${payment_detail.id}`} value={`${payment_detail.product.serial}`} placeholder={payment_detail.product.serial} disabled readOnly />
                                                            <Label htmlFor={`name-count-${payment_detail.id}`}>Cantidad del producto</Label>
                                                            <TextInput type="text" id={`name-count-${payment_detail.id}`} value={`${payment_detail.product.count}`} placeholder={`${payment_detail.product.count}`} disabled readOnly />
                                                            <Label htmlFor={`serial-price-${payment_detail.id}`}>Precio del producto</Label>
                                                            <TextInput type="text" id={`serial-price-${payment_detail.id}`} value={`$ ${Number(payment_detail.product.price).toFixed(2)}`} placeholder={`$ ${Number(payment_detail.product.price).toFixed(2)}`} disabled readOnly />
                                                        </div>
                                                    </Accordion.Content>
                                                </Accordion.Panel>
                                            ))
                                        }

                                    </Accordion>
                                </div>

                            </div>
                            <div className="flex justify-start items-center gap-2 h-auto">
                                <Button color="success" onClick={() => {
                                    setPaymentDetail((before) => ({ ...before, id: item.id.toString() }))
                                    setOpenModalAddProductToPayment(true)
                                }}>
                                    Agregar producto
                                </Button>
                                <Button color="primary" onClick={async() => {
                                    setPaymentDetail((before) => ({ ...before, id: item.id.toString() }))
                                    const response = await usePostFetch(SERVER_LOCAL, { path: `/api/v1/payments/${item.id.toString()}/mark_as_paid/`, tokenAuth: useGetLocalStorage('token') ?? "" })
                                    toast(response.detail, { type: "info" })
                                    await exec_data()
                                }}>
                                    Pagar producto
                                </Button>
                                <Button color="gray" onClick={async() => {
                                    setPaymentDetail((before) => ({ ...before, id: item.id.toString() }))
                                    const response = await usePostFetch(SERVER_LOCAL, { path: `/api/v1/payments/${item.id.toString()}/cancel/`, tokenAuth: useGetLocalStorage('token') ?? "" })
                                    toast(response.detail, { type: "info" })
                                    await exec_data()
                                }}>
                                    Cancelar factura
                                </Button>
                                <Button color="failure" onClick={async() => {
                                    setPaymentDetail((before) => ({ ...before, id: item.id.toString() }))
                                    const response = await useDeleteFetch(SERVER_LOCAL, { path: `/api/v1/payments/${item.id.toString()}/delete_cancelled_payments/`, tokenAuth: useGetLocalStorage('token') ?? "" })
                                    toast(response.detail, { type: "info" })
                                    await exec_data()
                                }}>
                                    Eliminar factura
                                </Button>
                            </div>
                            <div className="flex justify-end items-center gap-2 font-medium h-auto">
                                <div className="">
                                    <Badge color={STATUS_PAYMENT_COLOR[item.status-1]} icon={
                                        STATUS_PAYMENTS.payment === item.status ? HiBadgeCheck
                                        : STATUS_PAYMENTS.cancel === item.status ? MdOutlineCancel
                                        : STATUS_PAYMENTS.draft === item.status ? VscIssueDraft
                                        : undefined
                                    }>
                                        {STATUS_PAYMENT[item.status-1]}
                                    </Badge>
                                </div>
                                <div className="">
                                    <Badge color="gray" icon={HiClock}>
                                        {format(item.created_at, "full")}
                                    </Badge>
                                </div>
                            </div>
                            <HR />
                        </section>

                    ))
                }
                {
                    nextPage ?
                        <Button color="primary" onClick={async () => {
                            if (nextPage) {
                                const data = await useGetFetch<ResponseList<PaymentContent>>(nextPage, { tokenAuth: useGetLocalStorage('token') ?? "" }) as ResponseList<PaymentContent>
                                if (data?.results) {
                                    setNextPage(data.next)
                                    const results = data.results
                                    setInvoices((currentList) => ([...currentList, ...results]))
                                }
                            }
                        }}>
                            Ver más
                        </Button>
                        :
                        <></>
                }
            </Card>
        </>
    )

}