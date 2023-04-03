const in_datatime_begin_wish = document.getElementById('in_datatime_begin_wish')
const in_datatime_end_wish = document.getElementById('in_datatime_end_wish')

in_datatime_begin_with.addEventListener('change', function() {
    in_datatime_end_wish.min=in_datatime_begin_wish.value
    date = new Date(in_datatime_begin_wish.value)
    console.log(date)
    date.setDate(date.getDate() + 15)
    console.log(date)
    in_datatime_end_wish.max = date.toISOString().substring(0,10)

})