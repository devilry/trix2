$(function () {
    $('#datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    $('#datetimepicker2').datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false //Important! See issue #1075
    });
    $("#datetimepicker").on("dp.change", function (e) {
        $('#datetimepicker2').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker2").on("dp.change", function (e) {
        $('#datetimepicker').data("DateTimePicker").maxDate(e.date);
    });
});
